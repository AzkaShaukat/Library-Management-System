from app.database.db_handler import db

class ReportService:
    @staticmethod
    def get_all_books():
        query = "SELECT * FROM books ORDER BY title"
        return db.execute_query(query, fetch=True)

    @staticmethod
    def get_books_by_category(category):
        query = "SELECT * FROM books WHERE category = %s"
        return db.execute_query(query, (category,), fetch=True)

    @staticmethod
    def get_available_books():
        query = "SELECT * FROM books WHERE available_copies > 0"
        return db.execute_query(query, fetch=True)