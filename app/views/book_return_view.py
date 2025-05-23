import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.services.loan_service import LoanService
from app.services.book_service import BookService


class BookReturnView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Book Returns")
        self.geometry("1000x600")
        self._setup_widgets()
        self._load_active_loans()

    def _setup_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self._search_loans)

        # Treeview for active loans
        columns = [
            ("Loan ID", 70), ("Book ID", 70), ("Title", 200),
            ("Member ID", 80), ("Issue Date", 120), ("Due Date", 120),
            ("Days Overdue", 100), ("Estimated Fine", 100)
        ]

        self.loans_tree = ttk.Treeview(
            main_frame,
            columns=[col[0] for col in columns],
            show="headings"
        )

        for col, width in columns:
            self.loans_tree.heading(col, text=col)
            self.loans_tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.loans_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.loans_tree.configure(yscrollcommand=scrollbar.set)
        self.loans_tree.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="📚 Return Selected Book",
            command=self._return_book,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

    def _load_active_loans(self):
        """Load all active loans into the treeview"""
        for row in self.loans_tree.get_children():
            self.loans_tree.delete(row)

        loans = LoanService.get_active_loans()
        for loan in loans:
            due_date = loan['due_date']
            days_overdue = 0
            fine = 0.0

            if due_date:
                due_date = due_date if isinstance(due_date, datetime) else datetime.strptime(due_date,
                                                                                             '%Y-%m-%d %H:%M:%S')
                days_overdue = max(0, (datetime.now() - due_date).days)
                fine = days_overdue * 5.0  # $5 per day fine

            self.loans_tree.insert('', 'end', values=(
                loan['loan_id'],
                loan['book_id'],
                loan['title'],
                loan['member_id'],
                loan['issue_date'].strftime('%Y-%m-%d') if loan['issue_date'] else '',
                due_date.strftime('%Y-%m-%d') if due_date else '',
                days_overdue,
                f"${fine:.2f}"
            ))

    def _search_loans(self, event=None):
        """Search loans based on search term"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self._load_active_loans()
            return

        for row in self.loans_tree.get_children():
            self.loans_tree.delete(row)

        loans = LoanService.get_active_loans()
        for loan in loans:
            if (search_term in str(loan['loan_id']).lower() or
                    search_term in str(loan['book_id']).lower() or
                    search_term in loan['title'].lower() or
                    search_term in str(loan['member_id']).lower()):

                due_date = loan['due_date']
                days_overdue = 0
                fine = 0.0

                if due_date:
                    due_date = due_date if isinstance(due_date, datetime) else datetime.strptime(due_date,
                                                                                                 '%Y-%m-%d %H:%M:%S')
                    days_overdue = max(0, (datetime.now() - due_date).days)
                    fine = days_overdue * 5.0

                self.loans_tree.insert('', 'end', values=(
                    loan['loan_id'],
                    loan['book_id'],
                    loan['title'],
                    loan['member_id'],
                    loan['issue_date'].strftime('%Y-%m-%d') if loan['issue_date'] else '',
                    due_date.strftime('%Y-%m-%d') if due_date else '',
                    days_overdue,
                    f"${fine:.2f}"
                ))

    def _return_book(self):
        """Handle book return process"""
        selected = self.loans_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a loan to return")
            return

        loan_id = self.loans_tree.item(selected[0])['values'][0]
        book_title = self.loans_tree.item(selected[0])['values'][2]
        estimated_fine = self.loans_tree.item(selected[0])['values'][7]

        confirm_msg = f"Return '{book_title}'?"
        if estimated_fine != "$0.00":
            confirm_msg += f"\n\nThis book is overdue and will incur a fine of {estimated_fine}"

        if messagebox.askyesno("Confirm Return", confirm_msg, icon='question'):
            if LoanService.return_loan(loan_id):
                messagebox.showinfo("Success", "Book successfully returned")
                self._load_active_loans()
            else:
                messagebox.showerror("Error", "Failed to return book")