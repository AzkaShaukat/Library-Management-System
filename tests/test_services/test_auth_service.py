# tests/test_services/test_auth_service.py
import unittest
from app.services.auth_service import AuthService
from app.database.db_handler import db


class TestAuthService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup test data
        cls.test_username = "testuser_lms"
        cls.test_password = "testpassword123"

        # Hash the password
        import hashlib
        hashed_password = hashlib.sha256(cls.test_password.encode()).hexdigest()

        query = """
        INSERT INTO users (username, password, full_name, email, role)
        VALUES (%s, %s, %s, %s, %s)
        """
        db.execute_query(
            query,
            (cls.test_username, hashed_password, "Test User", "test@example.com", "librarian")
        )

    def test_successful_login(self):
        user = AuthService.login(self.test_username, self.test_password)
        self.assertIsNotNone(user)
        self.assertEqual(user.username, self.test_username)

    def test_failed_login_wrong_password(self):
        user = AuthService.login(self.test_username, "wrongpassword")
        self.assertIsNone(user)

    def test_failed_login_wrong_username(self):
        user = AuthService.login("nonexistentuser", self.test_password)
        self.assertIsNone(user)

    @classmethod
    def tearDownClass(cls):
        # Clean up test data
        query = "DELETE FROM users WHERE username = %s"
        db.execute_query(query, (cls.test_username,))


if __name__ == '__main__':
    unittest.main()