from datetime import datetime, timedelta


class Loan:
    def __init__(self, loan_id=None, book_id=None, member_id=None, issue_date=None,
                 due_date=None, return_date=None, loan_status='issued',
                 fine_amount=0.0, fine_status='none', issued_by=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = issue_date
        self.due_date = due_date
        self.return_date = return_date
        self.loan_status = loan_status
        self.fine_amount = fine_amount
        self.fine_status = fine_status  # 'none', 'pending', 'paid'
        self.issued_by = issued_by

    def calculate_fine(self, daily_rate=5.0):
        """Calculate fine based on overdue days"""
        if self.return_date and self.due_date:
            return_date = self.return_date if isinstance(self.return_date, datetime) else datetime.strptime(
                self.return_date, '%Y-%m-%d %H:%M:%S')
            due_date = self.due_date if isinstance(self.due_date, datetime) else datetime.strptime(self.due_date,
                                                                                                   '%Y-%m-%d %H:%M:%S')

            if return_date > due_date:
                days_overdue = (return_date - due_date).days
                return days_overdue * daily_rate
        return 0.0

    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'loan_status': self.loan_status,
            'fine_amount': self.fine_amount,
            'fine_status': self.fine_status,
            'issued_by': self.issued_by
        }