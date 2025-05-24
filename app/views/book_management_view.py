# book_management_view.py
import tkinter as tk
from tkinter import ttk, messagebox, font
from app.services.book_service import BookService
from app.services.user_service import UserService


class BookManagementView(tk.Toplevel):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("📚 Book Management")
        self.geometry("1250x780") # Slightly increased size
        self.minsize(1000, 600)

        # --- Theme Colors ---
        self.bg_color = '#f0f2f5'
        self.fg_color = '#ffffff'
        self.primary_color = '#3498db'
        self.primary_dark_color = '#2980b9'
        self.success_color = '#2ecc71'
        self.success_dark_color = '#27ae60'
        self.danger_color = '#e74c3c'
        self.danger_dark_color = '#c0392b'
        self.header_bg_color = '#2c3e50'
        self.header_fg_color = '#ffffff'
        self.text_color = '#212529'
        self.text_secondary_color = '#5e6c77'
        self.border_color = '#d1d8de'
        self.entry_bg_color = '#ffffff'

        # --- Fonts ---
        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_large_bold = (self.font_family, 12, "bold")
        self.font_title_section = (self.font_family, 16, "bold") # For view title
        self.font_treeview_heading = (self.font_family, 10, "bold")
        self.font_treeview_row = (self.font_family, 10)
        self.font_button = (self.font_family, 10, "bold")
        self.tree_row_height = 28
        self.entry_internal_padding = 6
        self.button_padding_y = 8

        self.configure(bg=self.bg_color)
        self._setup_styles()
        self._create_widgets()
        self._load_books()
        self.grab_set() # Make window modal over its parent

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.fg_color) # For card-like frames
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.font_normal)
        self.style.configure('Dialog.TLabel', background=self.fg_color, foreground=self.text_color, font=self.font_normal) # For dialogs
        self.style.configure('Header.TLabel', background=self.bg_color, foreground=self.header_bg_color, font=self.font_title_section)
        self.style.configure('Error.TLabel', background=self.fg_color, foreground=self.danger_color, font=self.font_normal)


        self.style.configure('Treeview', font=self.font_treeview_row, rowheight=self.tree_row_height,
                             fieldbackground=self.fg_color, background=self.fg_color, borderwidth=0, relief='flat')
        self.style.configure('Treeview.Heading', font=self.font_treeview_heading,
                             background=self.header_bg_color, foreground=self.header_fg_color,
                             padding=8, relief='flat')
        self.style.map('Treeview.Heading', background=[('active', self.primary_color)])

        self.style.configure('TButton', font=self.font_button, padding=(10, self.button_padding_y), relief='flat', borderwidth=0)
        self.style.configure('Primary.TButton', background=self.primary_color, foreground=self.fg_color)
        self.style.map('Primary.TButton', background=[('active', self.primary_dark_color), ('!disabled', self.primary_color)])
        self.style.configure('Success.TButton', background=self.success_color, foreground=self.fg_color)
        self.style.map('Success.TButton', background=[('active', self.success_dark_color), ('!disabled', self.success_color)])
        self.style.configure('Danger.TButton', background=self.danger_color, foreground=self.fg_color)
        self.style.map('Danger.TButton', background=[('active', self.danger_dark_color), ('!disabled', self.danger_color)])

        self.style.configure('TEntry', font=self.font_normal, padding=self.entry_internal_padding, relief='flat',
                             fieldbackground=self.entry_bg_color, bordercolor=self.border_color, lightcolor=self.border_color, darkcolor=self.border_color)
        self.style.map('TEntry', bordercolor=[('focus', self.primary_color)])


    def _create_widgets(self):
        # Main container
        outer_frame = ttk.Frame(self, padding=20) # Padding for the whole window
        outer_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(outer_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="Book Management", style='Header.TLabel').pack(side=tk.LEFT)

        # Content Card Frame
        content_card = ttk.Frame(outer_frame, style='Card.TFrame', padding=20)
        content_card.pack(fill=tk.BOTH, expand=True)
        # Apply a border to the card (using tk.Frame for simple border)
        content_card.configure(relief="solid", borderwidth=1) # Using relief on ttk.Frame
        # Or use a tk.Frame wrapper for border:
        # card_wrapper = tk.Frame(outer_frame, bg=self.border_color, bd=1)
        # card_wrapper.pack(fill=tk.BOTH, expand=True)
        # content_card = ttk.Frame(card_wrapper, style='Card.TFrame', padding=20)
        # content_card.pack(fill=tk.BOTH, expand=True, padx=1,pady=1)


        # Search frame
        search_frame = ttk.Frame(content_card, style='Card.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 15))

        search_icon_label = ttk.Label(search_frame, text="🔍", font=(self.font_family, 12), background=self.fg_color)
        search_icon_label.pack(side=tk.LEFT, padx=(0, 8))

        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10), ipady=2)
        self.search_entry.bind('<KeyRelease>', self._search_books)

        # Treeview frame
        tree_frame = ttk.Frame(content_card, style='Card.TFrame') # Ensure background matches card
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0,15))

        columns = [
            ("ID", 50), ("ISBN", 120), ("Title", 250), ("Author", 150),
            ("Publisher", 150), ("Year", 60), ("Category", 100),
            ("Total", 60), ("Available", 70), ("Shelf", 80), ("Added By", 120)
        ]

        self.tree = ttk.Treeview(
            tree_frame,
            columns=[col[0] for col in columns],
            show="headings",
            selectmode="browse",
            style='Treeview'
        )

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, minwidth=width, anchor="w") # Use minwidth and anchor "w"

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Place scrollbar next to treeview correctly
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill=tk.BOTH, expand=True)


        # Button frame
        button_frame = ttk.Frame(content_card, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))

        buttons_data = [
            ("➕ Add New", self._open_add_dialog, 'Success.TButton'),
            ("✏️ Update", self._open_update_dialog, 'Primary.TButton'),
            ("🗑️ Delete", self._delete_selected, 'Danger.TButton'),
            ("🔍 Details", self._view_book_details, 'TButton') # Standard TButton
        ]

        for text, command, style in buttons_data:
            btn = ttk.Button(button_frame, text=text, command=command, style=style)
            btn.pack(side=tk.LEFT, padx=(0,10))


    def _load_books(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        books = BookService.get_all_books()
        for book in books:
            added_by_name = UserService.get_user_name(book.added_by) or f"User #{book.added_by}"
            self.tree.insert('', 'end', values=(
                book.book_id,
                book.isbn,
                book.title,
                book.author,
                book.publisher,
                book.publication_year,
                book.category,
                book.total_copies,
                book.available_copies,
                book.shelf_location,
                added_by_name
            ))

    def _search_books(self, event=None):
        search_term = self.search_entry.get().lower()
        if not search_term:
            self._load_books()
            return

        for row in self.tree.get_children():
            self.tree.delete(row)

        books = BookService.get_all_books()
        for book in books:
            if (search_term in str(book.book_id).lower() or
                    search_term in book.isbn.lower() or
                    search_term in book.title.lower() or
                    search_term in book.author.lower() or
                    (book.publisher and search_term in book.publisher.lower()) or # Check for None
                    (book.category and search_term in book.category.lower())):    # Check for None
                added_by_name = UserService.get_user_name(book.added_by) or f"User #{book.added_by}"
                self.tree.insert('', 'end', values=(
                    book.book_id,
                    book.isbn,
                    book.title,
                    book.author,
                    book.publisher,
                    book.publication_year,
                    book.category,
                    book.total_copies,
                    book.available_copies,
                    book.shelf_location,
                    added_by_name
                ))

    def _open_add_dialog(self):
        self._book_dialog("Add New Book", self._save_new_book)

    def _open_update_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to update.", parent=self)
            return

        book_id = self.tree.item(selected[0])['values'][0]
        book = BookService.get_book_by_id(book_id)

        if book:
            self._book_dialog("Update Book", self._save_updated_book, book)

    def _view_book_details(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to view details.", parent=self)
            return

        book_id = self.tree.item(selected[0])['values'][0]
        book = BookService.get_book_by_id(book_id)

        if book:
            added_by_name = UserService.get_user_name(book.added_by) or f"User #{book.added_by}"
            details = (
                f"Book ID: {book.book_id}\n"
                f"ISBN: {book.isbn}\n"
                f"Title: {book.title}\n"
                f"Author: {book.author}\n"
                f"Publisher: {book.publisher or 'N/A'}\n"
                f"Year: {book.publication_year or 'N/A'}\n"
                f"Category: {book.category or 'N/A'}\n"
                f"Total Copies: {book.total_copies}\n"
                f"Available Copies: {book.available_copies}\n"
                f"Shelf Location: {book.shelf_location or 'N/A'}\n"
                f"Added By: {added_by_name}"
            )
            messagebox.showinfo("Book Details", details, parent=self)

    def _book_dialog(self, title_text, save_command, book=None):
        dialog = tk.Toplevel(self)
        dialog.title(title_text)
        dialog.geometry("450x580") # Adjusted size
        dialog.resizable(False, False)
        dialog.configure(bg=self.fg_color) # Dialog background
        dialog.grab_set()

        dialog_frame = ttk.Frame(dialog, padding=20, style='Card.TFrame') # Use Card.TFrame for fg_color
        dialog_frame.pack(fill=tk.BOTH, expand=True)


        error_label_dialog = ttk.Label(dialog_frame, text="", style='Error.TLabel') # Assign to instance if needed elsewhere
        error_label_dialog.grid(row=0, column=0, columnspan=2, pady=(0, 10), sticky="ew")


        fields_info = [
            ("isbn", "ISBN:", True), ("title", "Title:", True), ("author", "Author:", True),
            ("publisher", "Publisher:", False), ("publication_year", "Pub. Year:", False),
            ("category", "Category:", False), ("total_copies", "Total Copies:", True),
            ("available_copies", "Available Copies:", True), ("shelf_location", "Shelf Location:", False)
        ]
        entries = {}

        for i, (field_key, field_label, is_required) in enumerate(fields_info):
            label_text = field_label + (" *" if is_required else "")
            ttk.Label(dialog_frame, text=label_text, style='Dialog.TLabel').grid(
                row=i + 1, column=0, sticky="w", padx=5, pady=8) # pady increased

            entry = ttk.Entry(dialog_frame, width=35)
            entry.grid(row=i + 1, column=1, padx=5, pady=8, sticky="ew") # pady increased
            entries[field_key] = entry

            if book and hasattr(book, field_key):
                value = getattr(book, field_key)
                entry.insert(0, str(value) if value is not None else "")

        dialog_frame.columnconfigure(1, weight=1) # Make entry column expandable

        if book: # Store book_id for updates
            entries['book_id'] = book.book_id

        button_frame_dialog = ttk.Frame(dialog_frame, style='Card.TFrame')
        button_frame_dialog.grid(row=len(fields_info) + 1, column=0, columnspan=2, pady=(20, 0), sticky="e")


        save_btn = ttk.Button(
            button_frame_dialog, text="Save",
            command=lambda: save_command(dialog, entries, error_label_dialog), # Pass error_label
            style='Success.TButton'
        )
        save_btn.pack(side=tk.LEFT, padx=(0,10))

        cancel_btn = ttk.Button(
            button_frame_dialog, text="Cancel",
            command=dialog.destroy, style='TButton' # Standard button
        )
        cancel_btn.pack(side=tk.LEFT)

    def _validate_book_data(self, book_data, error_label_dialog):
        required_fields = ["isbn", "title", "author", "total_copies", "available_copies"]
        for field in required_fields:
            if not book_data.get(field):
                error_label_dialog.config(text=f"{field.replace('_', ' ').title()} is required.")
                return False

        try:
            total_copies = int(book_data['total_copies'])
            available_copies = int(book_data['available_copies'])
            if total_copies < 0 or available_copies < 0:
                error_label_dialog.config(text="Copies must be a non-negative number.")
                return False
            if available_copies > total_copies:
                error_label_dialog.config(text="Available copies cannot exceed total copies.")
                return False
            book_data['total_copies'] = total_copies
            book_data['available_copies'] = available_copies
        except ValueError:
            error_label_dialog.config(text="Copies must be valid numbers.")
            return False

        if book_data.get('publication_year') and book_data['publication_year'].strip():
            try:
                book_data['publication_year'] = int(book_data['publication_year'])
            except ValueError:
                error_label_dialog.config(text="Publication year must be a valid number.")
                return False
        else:
             book_data['publication_year'] = None # Handle empty string for year

        error_label_dialog.config(text="") # Clear error
        return True


    def _save_new_book(self, window, entries, error_label_dialog):
        book_data = {f: entries[f].get().strip() for f in [
            "isbn", "title", "author", "publisher",
            "publication_year", "category", "total_copies",
            "available_copies", "shelf_location"
        ]}
        book_data['added_by'] = self.current_user.user_id

        if not self._validate_book_data(book_data, error_label_dialog):
            return

        if BookService.add_book(book_data):
            window.destroy()
            self._load_books()
            messagebox.showinfo("Success", "Book added successfully.", parent=self)
        else:
            error_label_dialog.config(text="Failed to add book. ISBN may already exist or data is invalid.")

    def _save_updated_book(self, window, entries, error_label_dialog):
        book_data = {f: entries[f].get().strip() for f in [
            "isbn", "title", "author", "publisher",
            "publication_year", "category", "total_copies",
            "available_copies", "shelf_location"
        ]}
        book_data['book_id'] = entries['book_id']

        if not self._validate_book_data(book_data, error_label_dialog):
            return

        if BookService.update_book(book_data):
            window.destroy()
            self._load_books()
            messagebox.showinfo("Success", "Book updated successfully.", parent=self)
        else:
            error_label_dialog.config(text="Failed to update book. Data may be invalid.")

    def _delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a book to delete.", parent=self)
            return

        book_id = self.tree.item(selected[0])['values'][0]
        book_title = self.tree.item(selected[0])['values'][2]

        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{book_title}'?\nThis action cannot be undone!",
                icon='warning',
                parent=self
        ):
            if BookService.delete_book(book_id):
                messagebox.showinfo("Success", "Book deleted successfully.", parent=self)
                self._load_books()
            else:
                messagebox.showerror("Error", "Failed to delete book. Book may be currently loaned or part of other records.", parent=self)