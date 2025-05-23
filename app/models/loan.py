from datetime import datetime, timedelta

class Loan:
    def __init__(self, loan_id=None, book_id=None, member_id=None, issue_date=None,
                 due_date=None, return_date=None, loan_status='issued', issued_by=None):
        self.loan_id = loan_id
        self.book_id = book_id
        self.member_id = member_id
        self.issue_date = issue_date
        self.due_date = due_date if due_date else self._calculate_due_date()
        self.return_date = return_date
        self.loan_status = loan_status
        self.issued_by = issued_by

    def _calculate_due_date(self, loan_period_days=14):
        """Calculate due date as 14 days from issue date by default"""
        if self.issue_date:
            if isinstance(self.issue_date, str):
                issue_date = datetime.strptime(self.issue_date, '%Y-%m-%d %H:%M:%S')
            else:
                issue_date = self.issue_date
            return issue_date + timedelta(days=loan_period_days)
        return None

    def to_dict(self):
        return {
            'loan_id': self.loan_id,
            'book_id': self.book_id,
            'member_id': self.member_id,
            'issue_date': self.issue_date,
            'due_date': self.due_date,
            'return_date': self.return_date,
            'loan_status': self.loan_status,
            'issued_by': self.issued_by
        }