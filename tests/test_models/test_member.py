import pytest
from datetime import datetime
from app.models.member import Member


def test_member_creation():
    """Test basic member creation"""
    member = Member(
        member_id=1,
        first_name="John",
        last_name="Doe",
        cnic="1234567890123",
        email="john@example.com",
        phone="1234567890",
        address="123 Main St",
        city="New York",
        registration_date=datetime.now(),
        membership_status="active",
        registered_by=1
    )

    assert member.member_id == 1
    assert member.full_name == "John Doe"
    assert member.email == "john@example.com"
    assert member.membership_status == "active"


def test_member_to_dict():
    """Test the to_dict method"""
    member = Member(
        member_id=1,
        first_name="John",
        last_name="Doe"
    )

    member_dict = member.to_dict()
    assert member_dict['member_id'] == 1
    assert member_dict['full_name'] == "John Doe"
    assert 'registration_date' in member_dict