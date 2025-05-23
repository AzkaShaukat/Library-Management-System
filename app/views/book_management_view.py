import tkinter as tk
from tkinter import ttk, messagebox
from app.services.book_service import BookService
from app.services.user_service import UserService  # Add this import


class BookManagementView(tk.Toplevel):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("Book Management")
        self.geometry("1200x600")
        self._create_widgets()

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tree view for book list
        self.tree = ttk.Treeview(main_frame, columns=(
            "ID", "ISBN", "Title", "Author", "Publisher", "Year",
            "Category", "Total", "Available", "Shelf", "Added By"
        ), show="headings")

        # Configure columns
        columns = [
            ("ID", 50), ("ISBN", 120), ("Title", 200), ("Author", 150),
            ("Publisher", 150), ("Year", 60), ("Category", 120),
            ("Total", 60), ("Available", 80), ("Shelf", 80), ("Added By", 150)
        ]

        for col, width in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="➕ Add Book",
            command=self._open_add_dialog,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="✏️ Update Selected",
            command=self._open_update_dialog,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="❌ Delete Selected",
            command=self._delete_selected,
            style="Danger.TButton"
        ).pack(side=tk.LEFT, padx=5)

        self._load_books()

    def _load_books(self):
        """Load books into the treeview with added_by as name instead of ID"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        books = BookService.get_all_books()
        for book in books:
            # Get user name instead of ID
            added_by_name = UserService.get_user_name(book.added_by)
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
                added_by_name or f"User #{book.added_by}"  # Fallback if user not found
            ))

    def _open_add_dialog(self):
        """Open dialog to add new book"""
        self._book_dialog("Add New Book", self._save_new_book)

    def _open_update_dialog(self):
        """Open dialog to update selected book"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to update")
            return

        book_id = self.tree.item(selected[0])['values'][0]
        book = BookService.get_book_by_id(book_id)

        if book:
            self._book_dialog("Update Book", self._save_updated_book, book)

    def _book_dialog(self, title, save_command, book=None):
        """Create book entry/update dialog"""
        window = tk.Toplevel(self)
        window.title(title)
        window.resizable(False, False)

        # Error label
        self.error_label = ttk.Label(window, foreground="red")
        self.error_label.grid(row=0, columnspan=2, pady=5)

        fields = [
            "isbn", "title", "author", "publisher",
            "publication_year", "category", "total_copies",
            "available_copies", "shelf_location"
        ]
        entries = {}

        for i, field in enumerate(fields):
            ttk.Label(window, text=field.replace('_', ' ').title() + ":").grid(
                row=i + 1, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(window)
            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")
            entries[field] = entry

            # Pre-fill for update
            if book and hasattr(book, field):
                entry.insert(0, str(getattr(book, field)))

        # Store book_id for updates
        if book:
            entries['book_id'] = book.book_id

        button_frame = ttk.Frame(window)
        button_frame.grid(row=len(fields) + 2, columnspan=2, pady=10)

        ttk.Button(
            button_frame,
            text="Save",
            command=lambda: save_command(window, entries),
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="Cancel",
            command=window.destroy
        ).pack(side=tk.LEFT, padx=5)

    def _save_new_book(self, window, entries):
        """Save new book to database"""
        book_data = {f: entries[f].get() for f in [
            "isbn", "title", "author", "publisher",
            "publication_year", "category", "total_copies",
            "available_copies", "shelf_location"
        ]}
        book_data['added_by'] = self.current_user.user_id

        # Validate required fields
        if not book_data['isbn'] or not book_data['title'] or not book_data['author']:
            self.error_label.config(text="ISBN, Title and Author are required")
            return

        # Validate numeric fields
        try:
            book_data['total_copies'] = int(book_data['total_copies'])
            book_data['available_copies'] = int(book_data['available_copies'])
            if book_data['publication_year']:
                book_data['publication_year'] = int(book_data['publication_year'])
        except ValueError:
            self.error_label.config(text="Please enter valid numbers for copies and year")
            return

        if BookService.add_book(book_data):
            window.destroy()
            self._load_books()
            messagebox.showinfo("Success", "Book added successfully")
        else:
            self.error_label.config(text="Failed to add book. ISBN may already exist.")

    def _save_updated_book(self, window, entries):
        """Save updated book to database"""
        book_data = {f: entries[f].get() for f in [
            "isbn", "title", "author", "publisher",
            "publication_year", "category", "total_copies",
            "available_copies", "shelf_location"
        ]}
        book_data['book_id'] = entries['book_id']

        # Validate required fields
        if not book_data['isbn'] or not book_data['title'] or not book_data['author']:
            self.error_label.config(text="ISBN, Title and Author are required")
            return

        # Validate numeric fields
        try:
            book_data['total_copies'] = int(book_data['total_copies'])
            book_data['available_copies'] = int(book_data['available_copies'])
            if book_data['publication_year']:
                book_data['publication_year'] = int(book_data['publication_year'])
        except ValueError:
            self.error_label.config(text="Please enter valid numbers for copies and year")
            return

        if BookService.update_book(book_data):
            window.destroy()
            self._load_books()
            messagebox.showinfo("Success", "Book updated successfully")
        else:
            self.error_label.config(text="Failed to update book.")

    def _delete_selected(self):
        """Delete selected book with confirmation"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete")
            return

        book_id = self.tree.item(selected[0])['values'][0]
        book_title = self.tree.item(selected[0])['values'][2]

        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{book_title}'?\nThis action cannot be undone!",
                icon='warning'
        ):
            if BookService.delete_book(book_id):
                messagebox.showinfo("Success", "Book deleted successfully")
                self._load_books()
            else:
                messagebox.showerror("Error", "Failed to delete book")