# tests/test_models/test_user.py
import unittest
from app.models.user import User


class TestUserModel(unittest.TestCase):
    def test_user_creation(self):
        user = User(
            user_id=1,
            username="testuser",
            password="password",
            full_name="Test User",
            email="test@example.com",
            role="librarian"
        )

        self.assertEqual(user.user_id, 1)
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.full_name, "Test User")

    def test_to_dict(self):
        user = User(
            user_id=1,
            username="testuser",
            password="password",
            full_name="Test User",
            email="test@example.com",
            role="librarian"
        )

        user_dict = user.to_dict()
        self.assertEqual(user_dict['user_id'], 1)
        self.assertEqual(user_dict['username'], "testuser")
        self.assertNotIn('password', user_dict)  # Password shouldn't be in dict


if __name__ == '__main__':
    unittest.main()