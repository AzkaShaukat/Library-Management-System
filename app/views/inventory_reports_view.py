# inventory_reports_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.services.report_service import ReportService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from collections import defaultdict


class InventoryReportsView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("📊 Inventory Reports Dashboard")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        # Modern color scheme
        self.bg_color = "#f0f2f5"
        self.card_color = "#ffffff"
        self.header_color = "#2c3e50"
        self.primary_color = "#3498db"
        self.success_color = "#2ecc71"
        self.danger_color = "#e74c3c"
        self.text_color = "#212529"
        self.light_text = "#ffffff"

        self.configure(bg=self.bg_color)
        self._setup_styles()
        self._create_widgets()
        self.grab_set()

    def _setup_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.card_color)
        self.style.configure('TLabel', background=self.bg_color,
                             foreground=self.text_color, font=('Segoe UI', 10))
        self.style.configure('Header.TLabel', font=('Segoe UI', 16, 'bold'),
                             foreground=self.header_color)
        self.style.configure('Stats.TLabel', font=('Segoe UI', 12),
                             foreground=self.text_color)
        self.style.configure('StatsValue.TLabel', font=('Segoe UI', 24, 'bold'),
                             foreground=self.primary_color)

        # Treeview styles
        self.style.configure('Treeview', font=('Segoe UI', 10), rowheight=30,
                             fieldbackground=self.card_color, background=self.card_color,
                             borderwidth=0)
        self.style.configure('Treeview.Heading', font=('Segoe UI', 10, 'bold'),
                             background=self.header_color, foreground=self.light_text,
                             padding=8, relief='flat')
        self.style.map('Treeview.Heading',
                       background=[('active', self.primary_color)])

        # Notebook styles
        self.style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        self.style.configure('TNotebook.Tab', font=('Segoe UI', 11, 'bold'),
                             padding=(15, 8), background=self.bg_color,
                             foreground=self.text_color)
        self.style.map('TNotebook.Tab',
                       background=[('selected', self.card_color),
                                   ('active', self.primary_color)],
                       foreground=[('selected', self.primary_color),
                                   ('active', self.light_text)])

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 15))
        ttk.Label(header_frame, text="Inventory Reports Dashboard",
                  style='Header.TLabel').pack(side=tk.LEFT)

        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create all tabs
        self._create_statistics_tab()
        self._create_category_analysis_tab()
        self._create_all_books_tab()
        self._create_available_books_tab()

    def _create_tab_frame(self, tab_text):
        tab = ttk.Frame(self.notebook, style='Card.TFrame', padding=15)
        self.notebook.add(tab, text=tab_text)
        return tab

    def _create_all_books_tab(self):
        tab = self._create_tab_frame("📚 All Books")

        # Treeview frame
        tree_frame = ttk.Frame(tab, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview columns
        columns = [
            ("ID", 60), ("Title", 300), ("Author", 200),
            ("Category", 150), ("Total", 80), ("Available", 80), ("Shelf", 100)
        ]

        self.all_books_tree = ttk.Treeview(tree_frame, columns=[col[0] for col in columns],
                                           show="headings", style='Treeview')

        for col, width in columns:
            self.all_books_tree.heading(col, text=col)
            self.all_books_tree.column(col, width=width, anchor='w')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.all_books_tree.yview)
        self.all_books_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.all_books_tree.pack(side="left", fill=tk.BOTH, expand=True)

        # Load data
        self._load_all_books()

    def _create_available_books_tab(self):
        tab = self._create_tab_frame("✅ Available Books")

        # Treeview frame
        tree_frame = ttk.Frame(tab, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True)

        # Treeview columns
        columns = [
            ("ID", 60), ("Title", 320), ("Author", 220),
            ("Category", 150), ("Available", 100), ("Shelf", 120)
        ]

        self.available_books_tree = ttk.Treeview(tree_frame, columns=[col[0] for col in columns],
                                                 show="headings", style='Treeview')

        for col, width in columns:
            self.available_books_tree.heading(col, text=col)
            self.available_books_tree.column(col, width=width, anchor='w')

        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical",
                                  command=self.available_books_tree.yview)
        self.available_books_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.available_books_tree.pack(side="left", fill=tk.BOTH, expand=True)

        # Load data
        self._load_available_books()

    def _create_statistics_tab(self):
        tab = self._create_tab_frame("📊 Key Statistics")
        stats_data = self._get_statistics()

        # Stats container
        stats_container = ttk.Frame(tab, style='Card.TFrame')
        stats_container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Metrics to display
        metrics = [
            ("Total Unique Books", stats_data['total_unique_books']),
            ("Total Copies (All Books)", stats_data['total_copies_all']),
            ("Total Available Copies", stats_data['total_available_copies']),
            ("Unique Authors", stats_data['total_authors']),
            ("Unique Categories", stats_data['total_categories']),
            ("Books Currently Loaned", stats_data['books_on_loan'])
        ]

        # Create a grid of stats cards
        for i, (label, value) in enumerate(metrics):
            row, col = divmod(i, 2)  # 2 columns

            stat_box = ttk.Frame(stats_container, style='Card.TFrame', padding=20,
                                 relief='solid', borderwidth=1)
            stat_box.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            ttk.Label(stat_box, text=label, style='Stats.TLabel',
                      wraplength=180, anchor="center").pack(pady=(0, 10))
            ttk.Label(stat_box, text=str(value), style='StatsValue.TLabel',
                      anchor="center").pack()

            # Configure grid weights
            stats_container.columnconfigure(col, weight=1)
            stats_container.rowconfigure(row, weight=1)

    def _create_category_analysis_tab(self):
        tab = self._create_tab_frame("📈 Books by Category")
        category_data = self._get_category_stats()

        # Graph frame
        graph_frame = ttk.Frame(tab, style='Card.TFrame', padding=10,
                                relief='solid', borderwidth=1)
        graph_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        if not category_data:
            ttk.Label(graph_frame, text="No category data available",
                      style='Stats.TLabel').pack(pady=20)
            return

        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(9, 6), dpi=100)
        fig.patch.set_facecolor(self.card_color)
        ax.set_facecolor(self.card_color)

        categories = list(category_data.keys())
        counts = list(category_data.values())

        bars = ax.bar(categories, counts, color=self.primary_color)
        ax.set_title('Number of Books per Category', fontsize=12, pad=20)
        ax.set_ylabel('Number of Books', fontsize=10)
        ax.tick_params(axis='x', rotation=45, labelsize=9)
        ax.tick_params(axis='y', labelsize=9)
        ax.grid(axis='y', linestyle='--', alpha=0.5)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height)}', ha='center', va='bottom', fontsize=9)

        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def _load_all_books(self):
        for row in self.all_books_tree.get_children():
            self.all_books_tree.delete(row)

        books = ReportService.get_all_books()
        for book in books:
            self.all_books_tree.insert('', 'end', values=(
                book.get('book_id', 'N/A'),
                book.get('title', 'N/A'),
                book.get('author', 'N/A'),
                book.get('category', 'N/A'),
                book.get('total_copies', 0),
                book.get('available_copies', 0),
                book.get('shelf_location', 'N/A')
            ))

    def _load_available_books(self):
        for row in self.available_books_tree.get_children():
            self.available_books_tree.delete(row)

        books = ReportService.get_available_books()
        for book in books:
            self.available_books_tree.insert('', 'end', values=(
                book.get('book_id', 'N/A'),
                book.get('title', 'N/A'),
                book.get('author', 'N/A'),
                book.get('category', 'N/A'),
                book.get('available_copies', 0),
                book.get('shelf_location', 'N/A')
            ))

    def _get_statistics(self):
        all_books = ReportService.get_all_books()
        total_unique = len(all_books)
        total_copies = sum(book.get('total_copies', 0) for book in all_books)
        available_copies = sum(book.get('available_copies', 0) for book in all_books)

        authors = set(book.get('author') for book in all_books if book.get('author'))
        categories = set(book.get('category') for book in all_books if book.get('category'))

        # Calculate books on loan (simplified)
        books_on_loan = total_copies - available_copies

        return {
            'total_unique_books': total_unique,
            'total_copies_all': total_copies,
            'total_available_copies': available_copies,
            'total_authors': len(authors),
            'total_categories': len(categories),
            'books_on_loan': books_on_loan
        }

    def _get_category_stats(self):
        books = ReportService.get_all_books()
        category_counts = defaultdict(int)

        for book in books:
            cat = book.get('category')
            if cat:
                category_counts[cat] += book.get('total_copies', 0)

        return dict(sorted(category_counts.items(), key=lambda item: item[1], reverse=True))