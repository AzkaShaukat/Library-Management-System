from datetime import datetime, timedelta
from app.models.loan import Loan
import pytest



def test_loan_creation_with_dates():
    """Test loan creation with provided dates"""
    issue_date = datetime.now()
    due_date = issue_date + timedelta(days=14)

    loan = Loan(
        loan_id=1,
        book_id=101,
        member_id=201,
        issue_date=issue_date,
        due_date=due_date,
        loan_status='issued'
    )

    assert loan.loan_id == 1
    assert loan.book_id == 101
    assert loan.due_date == due_date
    assert loan.loan_status == 'issued'


def test_loan_creation_without_due_date():
    """Test loan creation with automatic due date calculation"""
    issue_date = datetime.now()
    loan = Loan(
        loan_id=1,
        book_id=101,
        member_id=201,
        issue_date=issue_date
    )

    assert loan.due_date == issue_date + timedelta(days=14)


def test_loan_to_dict():
    """Test the to_dict method"""
    loan = Loan(
        loan_id=1,
        book_id=101,
        member_id=201
    )

    loan_dict = loan.to_dict()
    assert loan_dict['loan_id'] == 1
    assert loan_dict['book_id'] == 101
    assert 'issue_date' in loan_dict


def test_loan_fine_calculation():
    """Test fine calculation for overdue loans"""
    # Create an overdue loan
    due_date = datetime.now() - timedelta(days=5)
    loan = Loan(
        loan_id=1,
        due_date=due_date,
        return_date=datetime.now()
    )

    # Should be 5 days overdue at $5/day = $25
    assert loan.calculate_fine() == 25.0


def test_no_fine_for_early_return():
    """Test no fine is calculated for books returned on time"""
    due_date = datetime.now() + timedelta(days=2)
    loan = Loan(
        loan_id=1,
        due_date=due_date,
        return_date=datetime.now()
    )

    assert loan.calculate_fine() == 0.0


def test_loan_to_dict_includes_fine_fields():
    """Test that to_dict() includes fine-related fields"""
    loan = Loan(
        loan_id=1,
        fine_amount=10.0,
        fine_status='pending'
    )

    loan_dict = loan.to_dict()
    assert loan_dict['fine_amount'] == 10.0
    assert loan_dict['fine_status'] == 'pending'