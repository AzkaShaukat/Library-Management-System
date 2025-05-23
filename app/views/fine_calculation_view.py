import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from app.services.loan_service import LoanService
from app.services.fine_service import FineService


class FineManagementView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Fine Management")
        self.geometry("1000x600")
        self._setup_widgets()
        self._load_fines()

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
        self.search_entry.bind('<KeyRelease>', self._search_fines)

        # Filter frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=5)

        ttk.Label(filter_frame, text="Filter by Status:").pack(side=tk.LEFT, padx=5)
        self.status_filter = ttk.Combobox(filter_frame, values=["All", "Pending", "Paid"])
        self.status_filter.current(0)
        self.status_filter.pack(side=tk.LEFT, padx=5)
        self.status_filter.bind("<<ComboboxSelected>>", self._filter_fines)

        # Treeview for fines
        columns = [
            ("Loan ID", 70), ("Book ID", 70), ("Title", 200),
            ("Member ID", 80), ("Fine Amount", 100), ("Status", 80),
            ("Due Date", 120), ("Return Date", 120)
        ]

        self.fines_tree = ttk.Treeview(
            main_frame,
            columns=[col[0] for col in columns],
            show="headings"
        )

        for col, width in columns:
            self.fines_tree.heading(col, text=col)
            self.fines_tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.fines_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.fines_tree.configure(yscrollcommand=scrollbar.set)
        self.fines_tree.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="💵 Mark as Paid",
            command=self._mark_paid,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🔄 Refresh",
            command=self._load_fines
        ).pack(side=tk.LEFT, padx=5)

    def _load_fines(self):
        """Load all fines into the treeview"""
        for row in self.fines_tree.get_children():
            self.fines_tree.delete(row)

        loans = LoanService.get_loans_with_fines()
        for loan in loans:
            self.fines_tree.insert('', 'end', values=(
                loan['loan_id'],
                loan['book_id'],
                loan['title'],
                loan['member_id'],
                f"${loan['fine_amount']:.2f}",
                loan['fine_status'].capitalize(),
                loan['due_date'].strftime('%Y-%m-%d') if loan['due_date'] else '',
                loan['return_date'].strftime('%Y-%m-%d') if loan['return_date'] else ''
            ))

    def _search_fines(self, event=None):
        """Search fines based on search term"""
        search_term = self.search_entry.get().lower()
        if not search_term:
            self._load_fines()
            return

        for row in self.fines_tree.get_children():
            self.fines_tree.delete(row)

        loans = LoanService.get_loans_with_fines()
        for loan in loans:
            if (search_term in str(loan['loan_id']).lower() or
                    search_term in str(loan['book_id']).lower() or
                    search_term in loan['title'].lower() or
                    search_term in str(loan['member_id']).lower()):
                self.fines_tree.insert('', 'end', values=(
                    loan['loan_id'],
                    loan['book_id'],
                    loan['title'],
                    loan['member_id'],
                    f"${loan['fine_amount']:.2f}",
                    loan['fine_status'].capitalize(),
                    loan['due_date'].strftime('%Y-%m-%d') if loan['due_date'] else '',
                    loan['return_date'].strftime('%Y-%m-%d') if loan['return_date'] else ''
                ))

    def _filter_fines(self, event=None):
        """Filter fines by status"""
        status_filter = self.status_filter.get().lower()
        if status_filter == "all":
            self._load_fines()
            return

        for row in self.fines_tree.get_children():
            self.fines_tree.delete(row)

        loans = LoanService.get_loans_with_fines()
        for loan in loans:
            if loan['fine_status'].lower() == status_filter:
                self.fines_tree.insert('', 'end', values=(
                    loan['loan_id'],
                    loan['book_id'],
                    loan['title'],
                    loan['member_id'],
                    f"${loan['fine_amount']:.2f}",
                    loan['fine_status'].capitalize(),
                    loan['due_date'].strftime('%Y-%m-%d') if loan['due_date'] else '',
                    loan['return_date'].strftime('%Y-%m-%d') if loan['return_date'] else ''
                ))

    def _mark_paid(self):
        """Mark selected fine as paid"""
        selected = self.fines_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a fine to mark as paid")
            return

        loan_id = self.fines_tree.item(selected[0])['values'][0]
        fine_amount = self.fines_tree.item(selected[0])['values'][4]

        if messagebox.askyesno(
                "Confirm Payment",
                f"Mark fine of {fine_amount} as paid?",
                icon='question'
        ):
            if FineService.mark_fine_as_paid(loan_id):
                messagebox.showinfo("Success", "Fine marked as paid")
                self._load_fines()
            else:
                messagebox.showerror("Error", "Failed to update fine status")