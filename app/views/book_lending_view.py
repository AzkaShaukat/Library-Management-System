import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
from app.services.book_service import BookService
from app.services.member_service import MemberService
from app.services.loan_service import LoanService
from app.services.user_service import UserService


class BookLendingView(tk.Toplevel):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("Book Lending")
        self.geometry("1000x700")
        self.resizable(False, False)

        self._setup_styles()
        self._create_widgets()
        self._load_available_books()
        self._load_members()  # Add this line to load members initially
        self._load_active_loans()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 10))
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 10))

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Tab 1: Lend Books
        lend_tab = ttk.Frame(self.notebook)
        self.notebook.add(lend_tab, text="📖 Lend Books")

        # Search frame
        search_frame = ttk.Frame(lend_tab)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search Book:").pack(side=tk.LEFT, padx=5)
        self.book_search_entry = ttk.Entry(search_frame, width=30)
        self.book_search_entry.pack(side=tk.LEFT, padx=5)
        self.book_search_entry.bind('<KeyRelease>', self._search_books)

        ttk.Label(search_frame, text="Search Member:").pack(side=tk.LEFT, padx=5)
        self.member_search_entry = ttk.Entry(search_frame, width=30)
        self.member_search_entry.pack(side=tk.LEFT, padx=5)
        self.member_search_entry.bind('<KeyRelease>', self._search_members)

        # Book and member selection frames
        selection_frame = ttk.Frame(lend_tab)
        selection_frame.pack(fill=tk.BOTH, expand=True)

        # Available books frame
        book_frame = ttk.LabelFrame(selection_frame, text="Available Books")
        book_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        columns = [
            ("ID", 50), ("Title", 200), ("Author", 150),
            ("Available", 80), ("Shelf", 80)
        ]

        self.books_tree = ttk.Treeview(
            book_frame,
            columns=[col[0] for col in columns],
            show="headings",
            selectmode="browse"
        )

        for col, width in columns:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(book_frame, orient="vertical", command=self.books_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.books_tree.configure(yscrollcommand=scrollbar.set)
        self.books_tree.pack(fill=tk.BOTH, expand=True)

        # Members frame
        member_frame = ttk.LabelFrame(selection_frame, text="Members")
        member_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        member_columns = [
            ("ID", 50), ("Name", 150), ("Phone", 120), ("Status", 80)
        ]

        self.members_tree = ttk.Treeview(
            member_frame,
            columns=[col[0] for col in member_columns],
            show="headings",
            selectmode="browse"
        )

        for col, width in member_columns:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(member_frame, orient="vertical", command=self.members_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.members_tree.configure(yscrollcommand=scrollbar.set)
        self.members_tree.pack(fill=tk.BOTH, expand=True)

        # Lend button
        button_frame = ttk.Frame(lend_tab)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="📚 Lend Selected Book to Selected Member",
            command=self._lend_book,
            style="Accent.TButton"
        ).pack(pady=5, ipadx=20, ipady=5)

        # Tab 2: Active Loans
        loans_tab = ttk.Frame(self.notebook)
        self.notebook.add(loans_tab, text="📝 Active Loans")

        # Active loans treeview
        loan_columns = [
            ("Loan ID", 70), ("Book ID", 70), ("Title", 200),
            ("Member", 150), ("Issue Date", 120), ("Due Date", 120)
        ]

        self.loans_tree = ttk.Treeview(
            loans_tab,
            columns=[col[0] for col in loan_columns],
            show="headings",
            selectmode="browse"
        )

        for col, width in loan_columns:
            self.loans_tree.heading(col, text=col)
            self.loans_tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(loans_tab, orient="vertical", command=self.loans_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.loans_tree.configure(yscrollcommand=scrollbar.set)
        self.loans_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Return button
        return_button_frame = ttk.Frame(loans_tab)
        return_button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            return_button_frame,
            text="↩️ Return Selected Book",
            command=self._return_book,
            style="Accent.TButton"
        ).pack(pady=5, ipadx=20, ipady=5)

    def _load_available_books(self):
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)

        books = BookService.get_all_books()
        for book in books:
            if book.available_copies > 0:
                self.books_tree.insert('', 'end', values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.available_copies,
                    book.shelf_location
                ))

    def _load_members(self):
        for row in self.members_tree.get_children():
            self.members_tree.delete(row)

        members = MemberService.get_all_members()
        for member in members:
            if member.membership_status == 'active':
                self.members_tree.insert('', 'end', values=(
                    member.member_id,
                    f"{member.first_name} {member.last_name}",
                    member.phone,
                    member.membership_status
                ))

    def _load_active_loans(self):
        for row in self.loans_tree.get_children():
            self.loans_tree.delete(row)

        loans = LoanService.get_active_loans()
        for loan in loans:
            issue_date = loan['issue_date'].strftime('%Y-%m-%d') if loan['issue_date'] else ''
            due_date = loan['due_date'].strftime('%Y-%m-%d') if loan['due_date'] else ''

            self.loans_tree.insert('', 'end', values=(
                loan['loan_id'],
                loan['book_id'],
                loan['title'],
                loan['member_name'],
                issue_date,
                due_date
            ))

    def _search_books(self, event=None):
        search_term = self.book_search_entry.get().lower()
        if not search_term:
            self._load_available_books()
            return

        for row in self.books_tree.get_children():
            self.books_tree.delete(row)

        books = BookService.get_all_books()
        for book in books:
            if (book.available_copies > 0 and
                    (search_term in book.title.lower() or
                     search_term in book.author.lower() or
                     search_term in str(book.book_id))):
                self.books_tree.insert('', 'end', values=(
                    book.book_id,
                    book.title,
                    book.author,
                    book.available_copies,
                    book.shelf_location
                ))

    def _search_members(self, event=None):
        search_term = self.member_search_entry.get()
        if not search_term:
            self._load_members()
            return

        for row in self.members_tree.get_children():
            self.members_tree.delete(row)

        members = MemberService.search_members(search_term)
        for member in members:
            if member.membership_status == 'active':
                self.members_tree.insert('', 'end', values=(
                    member.member_id,
                    f"{member.first_name} {member.last_name}",
                    member.phone,
                    member.membership_status
                ))

    def _lend_book(self):
        book_selection = self.books_tree.selection()
        member_selection = self.members_tree.selection()
        print(f"Book selection: {book_selection}")  # Debug
        print(f"Member selection: {member_selection}")  # Debug
        # ... rest of the method

        if not book_selection or not member_selection:
            messagebox.showwarning("Warning", "Please select both a book and a member")
            return

        book_id = self.books_tree.item(book_selection[0])['values'][0]
        member_id = self.members_tree.item(member_selection[0])['values'][0]

        try:
            if LoanService.issue_loan(book_id, member_id, self.current_user.user_id):
                messagebox.showinfo("Success", "Book successfully loaned to member")
                self._load_available_books()  # Refresh book list
                self._load_active_loans()  # Refresh loans list
                self._load_members()  # Refresh members list (in case status changes)
            else:
                messagebox.showerror("Error", "Failed to issue loan. Book may no longer be available.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def _return_book(self):
        loan_selection = self.loans_tree.selection()
        if not loan_selection:
            messagebox.showwarning("Warning", "Please select a loan to return")
            return

        loan_id = self.loans_tree.item(loan_selection[0])['values'][0]
        book_title = self.loans_tree.item(loan_selection[0])['values'][2]
        member_name = self.loans_tree.item(loan_selection[0])['values'][3]

        if messagebox.askyesno(
                "Confirm Return",
                f"Are you sure you want to return '{book_title}' from {member_name}?",
                icon='question'
        ):
            if LoanService.return_loan(loan_id):
                messagebox.showinfo("Success", "Book successfully returned")
                self._load_available_books()
                self._load_active_loans()
            else:
                messagebox.showerror("Error", "Failed to return book")