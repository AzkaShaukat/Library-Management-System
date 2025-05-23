from app.database.db_handler import db
from datetime import datetime, timedelta
from app.database.db_handler import db
from app.models.loan import Loan


class LoanService:
    # Update loan_service.py's issue_loan method
    @staticmethod
    def issue_loan(book_id, member_id, issued_by):
        # Check if book is available
        book_query = "SELECT available_copies FROM books WHERE book_id = %s"
        book_result = db.execute_query(book_query, (book_id,), fetch=True)

        if not book_result or book_result[0]['available_copies'] <= 0:
            return False

        # Create new loan
        loan_query = """
            INSERT INTO loans 
            (book_id, member_id, issue_date, due_date, issued_by)
            VALUES (%s, %s, %s, %s, %s)
        """
        issue_date = datetime.now()
        due_date = issue_date + timedelta(days=14)  # 2 weeks loan period

        loan_values = (
            book_id,
            member_id,
            issue_date,
            due_date,
            issued_by
        )

        # Update book inventory
        update_book_query = "UPDATE books SET available_copies = available_copies - 1 WHERE book_id = %s"

        try:
            # Start transaction
            db.execute_query("START TRANSACTION")

            # Create loan
            db.execute_query(loan_query, loan_values)

            # Update book inventory
            db.execute_query(update_book_query, (book_id,))

            # Commit transaction
            db.execute_query("COMMIT")
            return True
        except Exception as e:
            # Rollback on error
            db.execute_query("ROLLBACK")
            print(f"Error issuing loan: {e}")
            return False

    @staticmethod
    def get_active_loans(member_id=None):
        query = """
            SELECT l.*, b.title, b.isbn, 
                   CONCAT(m.first_name, ' ', m.last_name) AS member_name
            FROM loans l
            JOIN books b ON l.book_id = b.book_id
            JOIN members m ON l.member_id = m.member_id
            WHERE l.return_date IS NULL
        """

        if member_id:
            query += " AND l.member_id = %s"
            results = db.execute_query(query, (member_id,), fetch=True)
        else:
            results = db.execute_query(query, fetch=True)

        return results if results else []

    @staticmethod
    def get_loan_by_id(loan_id):
        query = """
            SELECT l.*, b.title, b.isbn, 
                   CONCAT(m.first_name, ' ', m.last_name) AS member_name
            FROM loans l
            JOIN books b ON l.book_id = b.book_id
            JOIN members m ON l.member_id = m.member_id
            WHERE l.loan_id = %s
        """
        result = db.execute_query(query, (loan_id,), fetch=True)
        return result[0] if result else None

    @staticmethod
    def return_loan(loan_id):
        """Process book return and calculate any fines"""
        # Get loan details
        loan_query = """
                SELECT * FROM loans 
                WHERE loan_id = %s AND return_date IS NULL
            """
        loan_result = db.execute_query(loan_query, (loan_id,), fetch=True)

        if not loan_result:
            return False

        loan = loan_result[0]
        return_date = datetime.now()
        fine_amount = 0.0

        # Calculate fine if overdue
        if loan['due_date'] and return_date > loan['due_date']:
            days_overdue = (return_date - loan['due_date']).days
            fine_amount = days_overdue * 5.0  # $5 per day

        # Update loan record
        update_query = """
                UPDATE loans SET
                return_date = %s,
                loan_status = 'returned',
                fine_amount = %s,
                fine_status = CASE WHEN %s > 0 THEN 'pending' ELSE 'none' END
                WHERE loan_id = %s
            """

        # Update book available copies
        book_query = "UPDATE books SET available_copies = available_copies + 1 WHERE book_id = %s"

        try:
            db.execute_query("START TRANSACTION")
            db.execute_query(update_query, (return_date, fine_amount, fine_amount, loan_id))
            db.execute_query(book_query, (loan['book_id'],))
            db.execute_query("COMMIT")
            return True
        except Exception as e:
            db.execute_query("ROLLBACK")
            print(f"Error returning loan: {e}")
            return False

    @staticmethod
    def get_loans_with_fines():
        """Get all loans with fines (pending or paid)"""
        query = """
                SELECT l.*, b.title, 
                       CONCAT(m.first_name, ' ', m.last_name) AS member_name
                FROM loans l
                JOIN books b ON l.book_id = b.book_id
                JOIN members m ON l.member_id = m.member_id
                WHERE l.fine_amount > 0
                ORDER BY l.fine_status, l.due_date
            """
        results = db.execute_query(query, fetch=True)
        return results if results else []

    @staticmethod
    def get_member_loan_history(member_id):
        query = """
            SELECT l.*, b.title, b.isbn
            FROM loans l
            JOIN books b ON l.book_id = b.book_id
            WHERE l.member_id = %s
            ORDER BY l.issue_date DESC
        """
        results = db.execute_query(query, (member_id,), fetch=True)
        return results if results else []