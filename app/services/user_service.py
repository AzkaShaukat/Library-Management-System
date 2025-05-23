from app.database.db_handler import db

class UserService:
    @staticmethod
    def get_user_name(user_id):
        query = "SELECT full_name FROM users WHERE user_id = %s"
        result = db.execute_query(query, (user_id,), fetch=True)
        return result[0]['full_name'] if result else None