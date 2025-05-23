import pytest
from unittest.mock import MagicMock, patch
from app.services.member_service import MemberService
from app.models.member import Member


@pytest.fixture
def mock_db():
    with patch('app.services.member_service.db') as mock:
        yield mock


def test_register_member_success(mock_db):
    """Test successful member registration"""
    mock_db.execute_query.return_value = True

    member_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'phone': '1234567890',
        'address': '123 Main St',
        'city': 'New York',
        'registered_by': 1
    }

    result = MemberService.register_member(member_data)
    assert result is True
    mock_db.execute_query.assert_called_once()


def test_get_member_by_id(mock_db):
    """Test getting member by ID"""
    mock_data = {
        'member_id': 1,
        'first_name': 'John',
        'last_name': 'Doe',
        'phone': '1234567890',
        'city': 'New York',
        'membership_status': 'active'
    }
    mock_db.execute_query.return_value = [mock_data]

    member = MemberService.get_member_by_id(1)
    assert isinstance(member, Member)
    assert member.member_id == 1
    assert member.full_name == "John Doe"


def test_search_members(mock_db):
    """Test member search functionality"""
    mock_data = [
        {
            'member_id': 1,
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '1234567890',
            'city': 'New York'
        }
    ]
    mock_db.execute_query.return_value = mock_data

    members = MemberService.search_members("John")
    assert len(members) == 1
    assert members[0].first_name == "John"