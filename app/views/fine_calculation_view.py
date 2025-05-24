# fine_calculation_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class FineService:
    @staticmethod
    def get_all_fines_detailed():
        return [
            {
                'fine_id': 1,
                'loan_id': 101,
                'book_title': 'Raja Gidh',
                'member_name': 'Ali Hassan',
                'amount': 5.00,
                'due_date': datetime(2024, 12, 1),
                'paid_date': None,
                'status': 'Pending'
            },
            {
                'fine_id': 2,
                'loan_id': 102,
                'book_title': 'Moth Smoke',
                'member_name': 'Fatima Ali',
                'amount': 10.00,
                'due_date': datetime(2024, 11, 15),
                'paid_date': datetime(2024, 12, 5),
                'status': 'Paid'
            }
        ]

    @staticmethod
    def mark_fine_as_paid(fine_id):
        return True  # Simulate success


class FineManagementView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("💰 Fine Management")
        self.geometry("1200x700")
        self.minsize(950, 600)

        self.bg_color = '#f0f2f5'
        self.fg_color = '#ffffff'
        self.primary_color = '#3498db'
        self.primary_dark_color = '#2980b9'
        self.success_color = '#2ecc71'
        self.success_dark_color = '#27ae60'
        self.danger_color = '#e74c3c'
        self.header_bg_color = '#2c3e50'
        self.header_fg_color = '#ffffff'
        self.text_color = '#212529'
        self.border_color = '#d1d8de'
        self.entry_bg_color = '#ffffff'

        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_title = (self.font_family, 16, "bold")
        self.tree_row_height = 28

        self.configure(bg=self.bg_color)
        self._setup_styles()
        self._create_widgets()
        self._load_fines_data()
        self.grab_set()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('Card.TFrame', background=self.fg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.font_normal)
        style.configure('Header.TLabel', background=self.bg_color, foreground=self.header_bg_color, font=self.font_title)
        style.configure('Treeview', font=self.font_normal, rowheight=self.tree_row_height,
                        fieldbackground=self.fg_color, background=self.fg_color)
        style.configure('Treeview.Heading', font=self.font_bold,
                        background=self.header_bg_color, foreground=self.header_fg_color)
        style.map('Treeview.Heading', background=[('active', self.primary_color)])
        style.configure('TButton', font=self.font_bold, padding=(10, 8), relief='flat')
        style.configure('Success.TButton', background=self.success_color, foreground='white')
        style.map('Success.TButton', background=[('active', self.success_dark_color)])
        style.configure('Primary.TButton', background=self.primary_color, foreground='white')
        style.map('Primary.TButton', background=[('active', self.primary_dark_color)])

    def _create_widgets(self):
        outer = ttk.Frame(self, padding=20)
        outer.pack(fill=tk.BOTH, expand=True)

        header = ttk.Frame(outer)
        header.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header, text="Fine Management", style='Header.TLabel').pack(side=tk.LEFT)

        card = ttk.Frame(outer, style='Card.TFrame', padding=20)
        card.pack(fill=tk.BOTH, expand=True)
        card.configure(relief="solid", borderwidth=1)

        filter_frame = ttk.Frame(card, style='Card.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(filter_frame, text="🔍 Search:", style='TLabel').pack(side=tk.LEFT)
        self.search_entry = ttk.Entry(filter_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(5, 20))
        self.search_entry.bind('<KeyRelease>', self._filter_data)

        ttk.Label(filter_frame, text="Status:", style='TLabel').pack(side=tk.LEFT)
        self.status_filter = ttk.Combobox(filter_frame, values=["All", "Pending", "Paid"], width=15, state="readonly")
        self.status_filter.current(0)
        self.status_filter.pack(side=tk.LEFT)
        self.status_filter.bind("<<ComboboxSelected>>", self._filter_data)

        tree_frame = ttk.Frame(card, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        cols = ["Fine ID", "Loan ID", "Book Title", "Member Name", "Amount", "Due Date", "Paid Date", "Status"]
        self.fines_tree = ttk.Treeview(tree_frame, columns=cols, show="headings")
        self.fines_tree.tag_configure('paid', foreground=self.success_dark_color)
        self.fines_tree.tag_configure('pending', foreground=self.danger_color)

        for col in cols:
            anchor = "w" if col in ["Book Title", "Member Name"] else "center"
            self.fines_tree.heading(col, text=col, anchor=anchor)
            self.fines_tree.column(col, width=120, anchor=anchor)

        scroll = ttk.Scrollbar(tree_frame, orient="vertical", command=self.fines_tree.yview)
        self.fines_tree.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right", fill="y")
        self.fines_tree.pack(side="left", fill=tk.BOTH, expand=True)

        btn_frame = ttk.Frame(card, style='Card.TFrame')
        btn_frame.pack(fill=tk.X, pady=(10, 0))

        ttk.Button(btn_frame, text="💵 Mark Selected as Paid", style="Success.TButton",
                   command=self._mark_paid).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="🔄 Refresh List", style="Primary.TButton",
                   command=self._load_fines_data).pack(side=tk.LEFT)

    def _load_fines_data(self, search_term=None, status=None):
        self.fines_tree.delete(*self.fines_tree.get_children())
        search_term = self.search_entry.get().lower().strip() if search_term is None else search_term
        status = self.status_filter.get() if status is None else status

        for fine in FineService.get_all_fines_detailed():
            fine_status = fine['status'].capitalize()
            if status != "All" and fine_status != status:
                continue
            if search_term and not any(search_term in str(fine.get(key, '')).lower()
                                       for key in ['fine_id', 'loan_id', 'book_title', 'member_name']):
                continue

            due_str = fine['due_date'].strftime("%Y-%m-%d") if fine['due_date'] else "N/A"
            paid_str = fine['paid_date'].strftime("%Y-%m-%d") if fine['paid_date'] else "N/A"
            amount_str = f"${fine['amount']:.2f}"
            tag = 'paid' if fine_status == 'Paid' else 'pending'

            self.fines_tree.insert('', 'end', values=(
                fine['fine_id'], fine['loan_id'], fine['book_title'], fine['member_name'],
                amount_str, due_str, paid_str, fine_status
            ), tags=(tag,))

    def _filter_data(self, event=None):
        self._load_fines_data()

    def _mark_paid(self):
        selected = self.fines_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a fine to mark as paid.", parent=self)
            return

        item = self.fines_tree.item(selected[0])
        fine_id = item['values'][0]
        status = item['values'][7]

        if status == "Paid":
            messagebox.showinfo("Already Paid", f"Fine ID {fine_id} is already marked as paid.", parent=self)
            return

        if messagebox.askyesno("Confirm", f"Mark fine ID {fine_id} as paid?", parent=self):
            if FineService.mark_fine_as_paid(fine_id):
                messagebox.showinfo("Success", f"Fine ID {fine_id} marked as paid.", parent=self)
                self._load_fines_data()
            else:
                messagebox.showerror("Error", "Failed to mark fine as paid.", parent=self)
