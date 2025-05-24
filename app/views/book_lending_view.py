# book_lending_view.py
import tkinter as tk
from tkinter import ttk, messagebox, font
from datetime import datetime, timedelta
from app.services.book_service import BookService
from app.services.member_service import MemberService
from app.services.loan_service import LoanService


# from app.services.user_service import UserService # Not directly used for display here but good to have if needed


class BookLendingView(tk.Toplevel):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("📖 Book Lending & Active Loans")
        self.geometry("1200x800")  # Adjusted size
        self.minsize(1000, 700)

        # --- Theme Colors ---
        self.bg_color = '#f0f2f5'
        self.fg_color = '#ffffff'
        self.primary_color = '#3498db'
        self.primary_dark_color = '#2980b9'
        self.success_color = '#2ecc71'
        self.success_dark_color = '#27ae60'
        self.header_bg_color = '#2c3e50'
        self.header_fg_color = '#ffffff'
        self.text_color = '#212529'
        self.text_secondary_color = '#5e6c77'  # For less prominent text
        self.border_color = '#d1d8de'
        self.entry_bg_color = '#ffffff'
        self.danger_color = '#e74c3c'  # For overdue items

        # --- Fonts ---
        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_large_bold = (self.font_family, 12, "bold")
        self.font_title_section = (self.font_family, 16, "bold")
        self.font_treeview_heading = (self.font_family, 10, "bold")
        self.font_treeview_row = (self.font_family, 10)
        self.font_button = (self.font_family, 10, "bold")
        self.font_tab = (self.font_family, 11, "bold")
        self.tree_row_height = 28
        self.entry_internal_padding = 6
        self.button_padding_y = 8

        self.configure(bg=self.bg_color)
        self._setup_styles()
        self._create_widgets()
        self._load_available_books()
        self._load_members()
        self._load_active_loans()
        self.grab_set()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.fg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.font_normal)
        self.style.configure('Card.TLabel', background=self.fg_color, foreground=self.text_color,
                             font=self.font_normal)  # Labels on cards
        self.style.configure('Header.TLabel', font=self.font_large_bold, foreground=self.header_bg_color,
                             background=self.bg_color)  # Section headers
        self.style.configure('TLabelframe', background=self.bg_color, bordercolor=self.border_color,
                             lightcolor=self.border_color, darkcolor=self.border_color)
        self.style.configure('TLabelframe.Label', background=self.bg_color, foreground=self.text_color,
                             font=self.font_bold)

        self.style.configure('Treeview', font=self.font_treeview_row, rowheight=self.tree_row_height,
                             fieldbackground=self.fg_color, background=self.fg_color, borderwidth=1, relief='solid')
        self.style.configure('Treeview.Heading', font=self.font_treeview_heading,
                             background=self.header_bg_color, foreground=self.header_fg_color,
                             padding=8, relief='flat')
        self.style.map('Treeview.Heading', background=[('active', self.primary_color)])

        self.style.configure('TButton', font=self.font_button, padding=(10, self.button_padding_y), relief='flat')
        self.style.configure('Primary.TButton', background=self.primary_color, foreground=self.fg_color)
        self.style.map('Primary.TButton',
                       background=[('active', self.primary_dark_color), ('!disabled', self.primary_color)])
        self.style.configure('Success.TButton', background=self.success_color,
                             foreground=self.fg_color)  # For lend/return buttons
        self.style.map('Success.TButton',
                       background=[('active', self.success_dark_color), ('!disabled', self.success_color)])

        self.style.configure('TEntry', font=self.font_normal, padding=self.entry_internal_padding, relief='flat',
                             fieldbackground=self.entry_bg_color)
        self.style.map('TEntry', bordercolor=[('focus', self.primary_color)])

        self.style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        self.style.configure('TNotebook.Tab', font=self.font_tab, padding=(12, 8), background=self.bg_color,
                             foreground=self.text_secondary_color, relief='flat', borderwidth=0)
        self.style.map('TNotebook.Tab',
                       background=[('selected', self.fg_color), ('active', self.primary_color)],
                       # Selected tab has fg_color (white) bg
                       foreground=[('selected', self.primary_color), ('active', self.fg_color)])

    def _create_widgets(self):
        main_outer_frame = ttk.Frame(self, padding=15)
        main_outer_frame.pack(fill=tk.BOTH, expand=True)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_outer_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(10, 0))

        # Tab 1: Lend Books
        lend_tab = ttk.Frame(self.notebook, style='Card.TFrame', padding=15)  # Use Card.TFrame for white bg
        self.notebook.add(lend_tab, text="📚 Lend Books")
        self._create_lend_tab_content(lend_tab)

        # Tab 2: Active Loans
        loans_tab = ttk.Frame(self.notebook, style='Card.TFrame', padding=15)  # Use Card.TFrame for white bg
        self.notebook.add(loans_tab, text="📝 Active Loans")
        self._create_loans_tab_content(loans_tab)

        # Add tags for overdue items in Treeview
        self.loans_tree.tag_configure('overdue', foreground=self.danger_color, font=(self.font_family, 10, 'bold'))

    def _create_lend_tab_content(self, parent_tab_frame):
        # Search frame
        search_controls_frame = ttk.Frame(parent_tab_frame, style='Card.TFrame')
        search_controls_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(search_controls_frame, text="Search Book:", style='Card.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.book_search_entry = ttk.Entry(search_controls_frame, width=30)
        self.book_search_entry.pack(side=tk.LEFT, padx=(0, 15), ipady=2)
        self.book_search_entry.bind('<KeyRelease>', self._search_books)

        ttk.Label(search_controls_frame, text="Search Member:", style='Card.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.member_search_entry = ttk.Entry(search_controls_frame, width=30)
        self.member_search_entry.pack(side=tk.LEFT, padx=(0, 5), ipady=2)
        self.member_search_entry.bind('<KeyRelease>', self._search_members)

        # Main content area for book and member selection (side by side)
        selection_area_frame = ttk.Frame(parent_tab_frame, style='Card.TFrame')
        selection_area_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Available books frame
        book_frame = ttk.LabelFrame(selection_area_frame, text="Available Books", style='TLabelframe')
        book_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        book_cols = [("ID", 40), ("Title", 220), ("Author", 130), ("Available", 70), ("Shelf", 70)]
        self.books_tree = ttk.Treeview(book_frame, columns=[col[0] for col in book_cols], show="headings",
                                       selectmode="browse", style='Treeview')
        for col, width in book_cols:
            self.books_tree.heading(col, text=col)
            self.books_tree.column(col, width=width, minwidth=width, anchor="w")

        book_scroll = ttk.Scrollbar(book_frame, orient="vertical", command=self.books_tree.yview)
        self.books_tree.configure(yscrollcommand=book_scroll.set)
        book_scroll.pack(side="right", fill="y")
        self.books_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Members frame
        member_frame = ttk.LabelFrame(selection_area_frame, text="Active Members", style='TLabelframe')
        member_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))

        member_cols = [("ID", 40), ("Name", 180), ("Phone", 100), ("Status", 70)]
        self.members_tree = ttk.Treeview(member_frame, columns=[col[0] for col in member_cols], show="headings",
                                         selectmode="browse", style='Treeview')
        for col, width in member_cols:
            self.members_tree.heading(col, text=col)
            self.members_tree.column(col, width=width, minwidth=width, anchor="w")

        member_scroll = ttk.Scrollbar(member_frame, orient="vertical", command=self.members_tree.yview)
        self.members_tree.configure(yscrollcommand=member_scroll.set)
        member_scroll.pack(side="right", fill="y")
        self.members_tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Lend button
        lend_button_frame = ttk.Frame(parent_tab_frame, style='Card.TFrame')
        lend_button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(
            lend_button_frame,
            text="✅ Lend Selected Book to Member",
            command=self._lend_book,
            style="Success.TButton"  # Use Success for positive action
        ).pack(pady=5, ipady=5, ipadx=10)

    def _create_loans_tab_content(self, parent_tab_frame):
        # Active loans treeview
        loan_cols = [
            ("Loan ID", 70), ("Book ID", 70), ("Title", 250),
            ("Member", 150), ("Issue Date", 110), ("Due Date", 110),
            ("Days Overdue", 90), ("Fine", 90)  # Renamed from Fine Amount
        ]
        self.loans_tree = ttk.Treeview(parent_tab_frame, columns=[col[0] for col in loan_cols], show="headings",
                                       selectmode="browse", style='Treeview')
        for col, width in loan_cols:
            self.loans_tree.heading(col, text=col)
            self.loans_tree.column(col, width=width, minwidth=width,
                                   anchor="center" if col not in ["Title", "Member"] else "w")

        loan_list_scroll = ttk.Scrollbar(parent_tab_frame, orient="vertical", command=self.loans_tree.yview)
        self.loans_tree.configure(yscrollcommand=loan_list_scroll.set)
        loan_list_scroll.pack(side="right", fill="y")
        self.loans_tree.pack(fill=tk.BOTH, expand=True, pady=(0, 15))

        # Return button frame
        return_button_frame = ttk.Frame(parent_tab_frame, style='Card.TFrame')
        return_button_frame.pack(fill=tk.X, pady=(10, 0))
        ttk.Button(
            return_button_frame,
            text="↩️ Process Return for Selected Loan",
            command=self._return_book,
            style="Primary.TButton"  # Changed to Primary, Success for Lend
        ).pack(pady=5, ipady=5, ipadx=10)

    def _load_available_books(self):
        for row in self.books_tree.get_children():
            self.books_tree.delete(row)
        books = BookService.get_all_books()
        for book in books:
            if book.available_copies > 0:
                self.books_tree.insert('', 'end', values=(
                    book.book_id, book.title, book.author,
                    book.available_copies, book.shelf_location or "N/A"
                ))

    def _load_members(self):
        for row in self.members_tree.get_children():
            self.members_tree.delete(row)
        members = MemberService.get_all_members()
        for member in members:
            if member.membership_status == 'active':
                self.members_tree.insert('', 'end', values=(
                    member.member_id, f"{member.first_name} {member.last_name}",
                    member.phone, member.membership_status
                ))

    def _load_active_loans(self):
        for row in self.loans_tree.get_children():
            self.loans_tree.delete(row)
        loans = LoanService.get_active_loans()  # This should return detailed loans

        for loan in loans:
            issue_date_str = loan['issue_date'].strftime('%Y-%m-%d') if loan['issue_date'] else 'N/A'
            due_date_obj = loan['due_date']
            due_date_str = due_date_obj.strftime('%Y-%m-%d') if due_date_obj else 'N/A'

            days_overdue = 0
            fine_amount_val = 0.0
            item_tags = ()

            if due_date_obj:
                # Ensure due_date_obj is datetime for comparison
                if isinstance(due_date_obj, str):  # Should ideally be datetime from service
                    try:
                        due_date_obj = datetime.strptime(due_date_obj, '%Y-%m-%d %H:%M:%S')  # Match your typical format
                    except ValueError:
                        due_date_obj = datetime.strptime(due_date_obj, '%Y-%m-%d')

                if datetime.now() > due_date_obj:
                    days_overdue = (datetime.now() - due_date_obj).days
                    fine_amount_val = days_overdue * 5.0  # Example fine rate
                    if days_overdue > 0:
                        item_tags = ('overdue',)

            fine_display = f"${fine_amount_val:.2f}" if fine_amount_val > 0 else "$0.00"

            self.loans_tree.insert('', 'end', values=(
                loan['loan_id'], loan['book_id'], loan['title'],
                loan['member_name'], issue_date_str, due_date_str,
                days_overdue if days_overdue > 0 else 0,
                fine_display
            ), tags=item_tags)

    def _search_books(self, event=None):
        search_term = self.book_search_entry.get().lower().strip()
        for row in self.books_tree.get_children(): self.books_tree.delete(row)
        books = BookService.get_all_books()
        for book in books:
            if book.available_copies > 0:
                if not search_term or \
                        search_term in book.title.lower() or \
                        search_term in book.author.lower() or \
                        search_term in str(book.book_id):
                    self.books_tree.insert('', 'end', values=(
                        book.book_id, book.title, book.author,
                        book.available_copies, book.shelf_location or "N/A"
                    ))

    def _search_members(self, event=None):
        search_term = self.member_search_entry.get().strip()
        for row in self.members_tree.get_children(): self.members_tree.delete(row)
        # Assuming MemberService.search_members handles empty search_term to return all active
        members = MemberService.search_members(search_term) if search_term else MemberService.get_all_members()
        for member in members:
            if member.membership_status == 'active':
                # If search_members doesn't filter by active, do it here.
                # Or ensure search_members also considers the "active" status if implied by context.
                if not search_term or \
                        search_term.lower() in f"{member.first_name} {member.last_name}".lower() or \
                        search_term in member.phone or \
                        search_term in str(member.member_id):
                    self.members_tree.insert('', 'end', values=(
                        member.member_id, f"{member.first_name} {member.last_name}",
                        member.phone, member.membership_status
                    ))

    def _lend_book(self):
        book_selection = self.books_tree.selection()
        member_selection = self.members_tree.selection()

        if not book_selection or not member_selection:
            messagebox.showwarning("Selection Required", "Please select both a book and a member.", parent=self)
            return

        book_id = self.books_tree.item(book_selection[0])['values'][0]
        member_id = self.members_tree.item(member_selection[0])['values'][0]

        try:
            if LoanService.issue_loan(book_id, member_id, self.current_user.user_id):
                messagebox.showinfo("Success", "Book successfully loaned to member.", parent=self)
                self._load_available_books()  # Refresh book list (availability changed)
                self._load_active_loans()  # Refresh active loans
                # No need to reload members unless their status changes upon loaning
            else:
                # More specific error if possible from LoanService
                messagebox.showerror("Loan Error",
                                     "Failed to issue loan. Book may no longer be available or member cannot borrow.",
                                     parent=self)
        except Exception as e:
            messagebox.showerror("System Error", f"An unexpected error occurred: {str(e)}", parent=self)
            print(f"Error during loan: {e}")  # Log for debugging

    def _return_book(self):
        loan_selection = self.loans_tree.selection()
        if not loan_selection:
            messagebox.showwarning("Selection Required", "Please select a loan to return.", parent=self)
            return

        selected_item_values = self.loans_tree.item(loan_selection[0])['values']
        loan_id = selected_item_values[0]
        book_title = selected_item_values[2]
        member_name = selected_item_values[3]
        fine_text = selected_item_values[7]  # Fine amount as text e.g., "$5.00"

        confirm_msg = f"Are you sure you want to process the return for '{book_title}' by {member_name}?"
        if fine_text != "$0.00":  # Check if there's a fine
            confirm_msg += f"\n\nThis loan has an outstanding fine of {fine_text}."
        confirm_msg += "\nProceed with the return?"

        if messagebox.askyesno("Confirm Return", confirm_msg, icon='question', parent=self):
            try:
                if LoanService.return_loan(loan_id):  # This service method should handle fine creation/update if any
                    messagebox.showinfo("Success", "Book successfully returned.", parent=self)
                    self._load_available_books()  # Book availability changes
                    self._load_active_loans()  # Loan becomes inactive or removed
                else:
                    messagebox.showerror("Return Error",
                                         "Failed to process book return. Please check loan status or contact support.",
                                         parent=self)
            except Exception as e:
                messagebox.showerror("System Error", f"An unexpected error occurred during return: {str(e)}",
                                     parent=self)
                print(f"Error during return: {e}")