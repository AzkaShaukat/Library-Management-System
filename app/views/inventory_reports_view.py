import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from app.services.report_service import ReportService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict


class InventoryReportsView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Inventory Reports Dashboard")
        self.geometry("1200x700")
        self._create_widgets()
        self._setup_styles()

    def _setup_styles(self):
        style = ttk.Style()
        style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'))
        style.configure('Graph.TFrame', background='white')
        style.configure('Stats.TFrame', background='#f0f0f0')

    def _create_widgets(self):
        # Main notebook for tabs
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: All Books
        self._create_all_books_tab()

        # Tab 2: Available Books
        self._create_available_books_tab()

        # Tab 3: Statistics
        self._create_statistics_tab()

        # Tab 4: Category Analysis
        self._create_category_analysis_tab()

    def _create_all_books_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📚 All Books")

        # Treeview for book list
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.all_books_tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Title", "Author", "Category", "Total", "Available", "Shelf"
        ), show="headings")

        # Configure columns
        columns = [
            ("ID", 50), ("Title", 250), ("Author", 150),
            ("Category", 120), ("Total", 60), ("Available", 80), ("Shelf", 80)
        ]

        for col, width in columns:
            self.all_books_tree.heading(col, text=col)
            self.all_books_tree.column(col, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.all_books_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.all_books_tree.configure(yscrollcommand=scrollbar.set)
        self.all_books_tree.pack(fill=tk.BOTH, expand=True)

        # Load data
        self._load_all_books()

    def _create_available_books_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="✅ Available Books")

        # Treeview for available books
        tree_frame = ttk.Frame(tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.available_books_tree = ttk.Treeview(tree_frame, columns=(
            "ID", "Title", "Author", "Category", "Available", "Shelf"
        ), show="headings")

        # Configure columns
        columns = [
            ("ID", 50), ("Title", 300), ("Author", 150),
            ("Category", 120), ("Available", 80), ("Shelf", 80)
        ]

        for col, width in columns:
            self.available_books_tree.heading(col, text=col)
            self.available_books_tree.column(col, width=width, anchor="center")

        # Add scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.available_books_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.available_books_tree.configure(yscrollcommand=scrollbar.set)
        self.available_books_tree.pack(fill=tk.BOTH, expand=True)

        # Load data
        self._load_available_books()

    def _create_statistics_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📊 Statistics")

        # Create frames for stats and graphs
        stats_frame = ttk.Frame(tab, style='Stats.TFrame')
        stats_frame.pack(fill=tk.X, padx=10, pady=10)

        # Statistics labels
        stats_data = self._get_statistics()

        ttk.Label(stats_frame, text=f"📖 Total Books: {stats_data['total_books']}",
                  font=('Helvetica', 12)).pack(side=tk.LEFT, padx=20)
        ttk.Label(stats_frame, text=f"✅ Available: {stats_data['available_books']}",
                  font=('Helvetica', 12)).pack(side=tk.LEFT, padx=20)
        ttk.Label(stats_frame, text=f"🔖 Categories: {stats_data['total_categories']}",
                  font=('Helvetica', 12)).pack(side=tk.LEFT, padx=20)
        ttk.Label(stats_frame, text=f"👥 Authors: {stats_data['total_authors']}",
                  font=('Helvetica', 12)).pack(side=tk.LEFT, padx=20)

        # Graph frame
        graph_frame = ttk.Frame(tab, style='Graph.TFrame')
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create availability pie chart
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
        ax.pie(
            [stats_data['available_books'],
             stats_data['total_books'] - stats_data['available_books']],
            labels=['Available', 'Checked Out'],
            autopct='%1.1f%%',
            colors=['#4CAF50', '#F44336'],
            startangle=90
        )
        ax.set_title('Book Availability')

        # Embed the pie chart
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def _create_category_analysis_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="📈 Category Analysis")

        # Get category data
        category_data = self._get_category_stats()
        categories = list(category_data.keys())
        counts = list(category_data.values())

        # Create frame for the bar chart
        graph_frame = ttk.Frame(tab, style='Graph.TFrame')
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create bar chart
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='white')
        bars = ax.bar(categories, counts, color='#2196F3')
        ax.set_title('Books by Category')
        ax.set_ylabel('Number of Books')
        ax.tick_params(axis='x', rotation=45)

        # Add value labels on bars
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}',
                    ha='center', va='bottom')

        # Embed the bar chart
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _load_all_books(self):
        for row in self.all_books_tree.get_children():
            self.all_books_tree.delete(row)

        books = ReportService.get_all_books()
        for book in books:
            self.all_books_tree.insert('', 'end', values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['total_copies'],
                book['available_copies'],
                book['shelf_location']
            ))

    def _load_available_books(self):
        for row in self.available_books_tree.get_children():
            self.available_books_tree.delete(row)

        books = ReportService.get_available_books()
        for book in books:
            self.available_books_tree.insert('', 'end', values=(
                book['book_id'],
                book['title'],
                book['author'],
                book['category'],
                book['available_copies'],
                book['shelf_location']
            ))

    def _get_statistics(self):
        books = ReportService.get_all_books()
        available = ReportService.get_available_books()

        # Get unique authors
        authors = set(book['author'] for book in books)

        # Get unique categories
        categories = set(book['category'] for book in books)

        return {
            'total_books': len(books),
            'available_books': len(available),
            'total_authors': len(authors),
            'total_categories': len(categories)
        }

    def _get_category_stats(self):
        books = ReportService.get_all_books()
        category_counts = defaultdict(int)

        for book in books:
            category_counts[book['category']] += 1

        return dict(category_counts)