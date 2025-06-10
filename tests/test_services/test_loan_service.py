import pytest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from app.services.loan_service import LoanService

@pytest.fixture
def mock_db():
    with patch('app.services.loan_service.db') as mock:
        mock.execute_query.side_effect = [
            [{'available_copies': 1}],  # First call - book check
            None,  # Second call - loan creation
            None  # Third call - book update
        ]
        yield mock


def test_issue_loan_success(mock_db):
    """Test successful book loan issuance"""
    # Mock the datetime.now() call
    with patch('app.services.loan_service.datetime') as mock_datetime:
        test_now = datetime(2023, 1, 1)
        mock_datetime.now.return_value = test_now

        result = LoanService.issue_loan(book_id=1, member_id=1, issued_by=1)

        assert result is True
        # Verify transaction was used
        mock_db.execute_query.assert_any_call("START TRANSACTION")
        mock_db.execute_query.assert_any_call("COMMIT")

        # Verify the loan query
        loan_query = mock_db.execute_query.call_args_list[2][0][0]
        assert "INSERT INTO loans" in loan_query
        assert "(book_id, member_id, issue_date, due_date, issued_by)" in loan_query

        # Verify the book update query
        update_query = mock_db.execute_query.call_args_list[3][0][0]
        assert "UPDATE books SET available_copies" in update_query


def test_issue_loan_no_available_copies():
    """Test loan issuance when no copies available"""
    with patch('app.services.loan_service.db') as mock_db:
        mock_db.execute_query.return_value = [{'available_copies': 0}]

        result = LoanService.issue_loan(book_id=1, member_id=1, issued_by=1)
        assert result is False
        mock_db.execute_query.assert_called_once()


def test_return_loan_success():
    """Test successful book return"""
    with patch('app.services.loan_service.db') as mock_db:
        mock_db.execute_query.return_value = True

        result = LoanService.return_loan(loan_id=1)
        assert result is True
        mock_db.execute_query.assert_called_once()


def test_get_active_loans():
    """Test retrieving active loans"""
    test_data = [{
        'loan_id': 1,
        'book_id': 1,
        'title': 'Test Book',
        'member_name': 'John Doe',
        'issue_date': datetime.now(),
        'due_date': datetime.now() + timedelta(days=14),
        'return_date': None
    }]

    with patch('app.services.loan_service.db') as mock_db:
        mock_db.execute_query.return_value = test_data

        loans = LoanService.get_active_loans()
        assert len(loans) == 1
        assert loans[0]['title'] == 'Test Book'
        assert loans[0]['return_date'] is None


@pytest.fixture
def mock_db():
    with patch('app.services.loan_service.db') as mock:
        yield mock


def test_return_loan_with_fine(mock_db):
    """Test returning an overdue loan calculates fine"""
    # Mock database responses
    mock_db.execute_query.side_effect = [
        [{
            'loan_id': 1,
            'book_id': 101,
            'due_date': datetime.now() - timedelta(days=3)
        }],  # Loan query
        None,  # Update loan
        None  # Update book
    ]

    result = LoanService.return_loan(1)
    assert result is True
    # Verify fine amount was calculated (3 days * $5 = $15)
    assert "fine_amount = 15.0" in mock_db.execute_query.call_args_list[1][0][0]


def test_return_loan_no_fine(mock_db):
    """Test returning a loan on time has no fine"""
    mock_db.execute_query.side_effect = [
        [{
            'loan_id': 1,
            'book_id': 101,
            'due_date': datetime.now() + timedelta(days=1)
        }],
        None,
        None
    ]

    result = LoanService.return_loan(1)
    assert result is True
    assert "fine_amount = 0.0" in mock_db.execute_query.call_args_list[1][0][0]


def test_get_loans_with_fines(mock_db):
    """Test retrieving loans with fines"""
    test_data = [{
        'loan_id': 1,
        'fine_amount': 10.0,
        'fine_status': 'pending',
        'title': 'Test Book'
    }]
    mock_db.execute_query.return_value = test_data

    loans = LoanService.get_loans_with_fines()
    assert len(loans) == 1
    assert loans[0]['fine_amount'] == 10.0