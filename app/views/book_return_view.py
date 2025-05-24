# book_return_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.services.loan_service import LoanService


class BookReturnView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("↩️ Book Returns Management")
        self.geometry("1150x700")
        self.minsize(900, 550)

        # Theme Colors
        self.bg_color = '#f0f2f5'
        self.fg_color = '#ffffff'
        self.primary_color = '#3498db'
        self.success_color = '#2ecc71'
        self.danger_color = '#e74c3c'
        self.header_bg_color = '#2c3e50'
        self.text_color = '#212529'
        self.border_color = '#d1d8de'

        # Fonts
        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_title = (self.font_family, 16, "bold")
        self.font_treeview = (self.font_family, 10)
        self.font_button = (self.font_family, 10, "bold")

        self.configure(bg=self.bg_color)
        self._setup_styles()
        self._create_widgets()
        self._load_active_loans()
        self.grab_set()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.fg_color)
        self.style.configure('TLabel', background=self.bg_color,
                             foreground=self.text_color, font=self.font_normal)
        self.style.configure('Header.TLabel', font=self.font_title,
                             foreground=self.header_bg_color)
        self.style.configure('Treeview', font=self.font_treeview, rowheight=30,
                             fieldbackground=self.fg_color, background=self.fg_color)
        self.style.configure('Treeview.Heading', font=self.font_bold,
                             background=self.header_bg_color, foreground='white')
        self.style.map('Treeview.Heading',
                       background=[('active', self.primary_color)])

        # Button styles
        self.style.configure('TButton', font=self.font_button, padding=8)
        self.style.configure('Primary.TButton', background=self.primary_color,
                             foreground='white')
        self.style.configure('Success.TButton', background=self.success_color,
                             foreground='white')

        # Treeview tags for overdue items
        self.style.configure('Overdue.Treeview', foreground=self.danger_color)

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame, text="Book Returns Management",
                  style='Header.TLabel').pack(side=tk.LEFT)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(search_frame, text="🔍 Search:").pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.search_entry.bind('<KeyRelease>', self._search_loans)

        # Treeview frame
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        columns = [
            ("Loan ID", 70), ("Book ID", 70), ("Title", 250),
            ("Member ID", 80), ("Member Name", 150),
            ("Issue Date", 110), ("Due Date", 110),
            ("Days Overdue", 90), ("Fine Amount", 100), ("Status", 80)
        ]

        self.loans_tree = ttk.Treeview(tree_frame, columns=[col[0] for col in columns],
                                       show="headings")

        for col, width in columns:
            anchor = "w" if col in ["Title", "Member Name"] else "center"
            self.loans_tree.heading(col, text=col)
            self.loans_tree.column(col, width=width, anchor=anchor)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.loans_tree.yview)
        self.loans_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.loans_tree.pack(side="left", fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(button_frame, text="↩️ Process Return",
                   command=self._return_book,
                   style='Success.TButton').pack()

    def _load_active_loans(self, search_term=None):
        for row in self.loans_tree.get_children():
            self.loans_tree.delete(row)

        # Use get_active_loans() instead of get_active_loans_detailed()
        loans = LoanService.get_active_loans()

        for loan in loans:
            issue_date = loan.get('issue_date', 'N/A')
            due_date = loan.get('due_date', 'N/A')

            # Calculate days overdue
            days_overdue = 0
            fine_amount = 0
            tags = ()

            if isinstance(due_date, str) and due_date != 'N/A':
                try:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d')
                    if datetime.now() > due_date:
                        days_overdue = (datetime.now() - due_date).days
                        fine_amount = days_overdue * 5.0  # $5 per day
                        tags = ('overdue',)
                except ValueError:
                    pass

            self.loans_tree.insert('', 'end', values=(
                loan.get('loan_id', 'N/A'),
                loan.get('book_id', 'N/A'),
                loan.get('title', 'N/A'),
                loan.get('member_id', 'N/A'),
                loan.get('member_name', 'N/A'),
                str(issue_date),
                str(due_date),
                days_overdue,
                f"${fine_amount:.2f}",
                "Overdue" if days_overdue > 0 else "Active"
            ), tags=tags)

    def _search_loans(self, event=None):
        search_term = self.search_entry.get().lower()
        for item in self.loans_tree.get_children():
            values = [str(v).lower() for v in self.loans_tree.item(item)['values']]
            if any(search_term in v for v in values):
                self.loans_tree.selection_set(item)
                self.loans_tree.focus(item)
                self.loans_tree.see(item)
                break

    def _return_book(self):
        selected = self.loans_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a loan to return", parent=self)
            return

        loan_id = self.loans_tree.item(selected[0])['values'][0]
        book_title = self.loans_tree.item(selected[0])['values'][2]
        member_name = self.loans_tree.item(selected[0])['values'][4]

        if messagebox.askyesno("Confirm Return",
                               f"Return '{book_title}' for {member_name}?",
                               parent=self):
            if LoanService.return_loan(loan_id):
                messagebox.showinfo("Success", "Book returned successfully", parent=self)
                self._load_active_loans()
            else:
                messagebox.showerror("Error", "Failed to return book", parent=self)