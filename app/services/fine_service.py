
from app.database.db_handler import db

class FineService:
    @staticmethod
    def mark_fine_as_paid(loan_id):
        """Update fine status to paid"""
        query = """
            UPDATE loans SET
            fine_status = 'paid'
            WHERE loan_id = %s AND fine_amount > 0
        """
        return db.execute_query(query, (loan_id,))

    @staticmethod
    def get_total_pending_fines():
        """Get sum of all pending fines"""
        query = "SELECT SUM(fine_amount) AS total FROM loans WHERE fine_status = 'pending'"
        result = db.execute_query(query, fetch=True)
        return result[0]['total'] if result and result[0]['total'] else 0.0

    @staticmethod
    def get_member_fines(member_id):
        """Get all fines for a specific member"""
        query = """
            SELECT l.*, b.title
            FROM loans l
            JOIN books b ON l.book_id = b.book_id
            WHERE l.member_id = %s AND l.fine_amount > 0
            ORDER BY l.fine_status, l.due_date
        """
        results = db.execute_query(query, (member_id,), fetch=True)
        return results if results else []