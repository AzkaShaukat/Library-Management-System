# app/services/auth_service.py
from app.models.user import User
from app.database.db_handler import db


class AuthService:
    @staticmethod
    def login(username, password):
        """Authenticate user"""
        try:
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            result = db.execute_query(query, (username, password), fetch=True)

            if result:
                user_data = result[0]
                return User(
                    user_id=user_data['user_id'],
                    username=user_data['username'],
                    password=user_data['password'],
                    full_name=user_data['full_name'],
                    email=user_data['email'],
                    role=user_data['role']
                )
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None

    @staticmethod
    def logout():
        """Logout user"""
        return True