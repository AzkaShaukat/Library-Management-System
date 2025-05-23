# app/views/admin_panel_view.py
import tkinter as tk
from tkinter import ttk, font
from app.services.auth_service import AuthService
from app.views.book_management_view import BookManagementView
from app.views.inventory_reports_view import InventoryReportsView
from app.views.member_registration_view import MemberRegistrationView
from app.views.book_lending_view import BookLendingView
from app.views.book_return_view import BookReturnView
from app.views.fine_calculation_view import FineManagementView


class AdminPanelView(tk.Tk):
    def __init__(self, user, on_logout):
        super().__init__()
        self.user = user
        self.on_logout = on_logout

        self.title(f"Library Management System - {user.full_name}")
        self.geometry("1200x700")
        self.minsize(1200, 700)

        # Custom fonts
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")
        self.button_font = font.Font(family="Helvetica", size=14)
        self.list_font = font.Font(family="Helvetica", size=16)
        self.icon_font = font.Font(family="Helvetica", size=70)  # Bigger icon font
        self.small_font = font.Font(family="Helvetica", size=14)

        # Configure styles
        self.style = ttk.Style()
        self.style.configure('Header.TFrame', background='#2c3e50')
        self.style.configure('Header.TLabel', background='#2c3e50', foreground='white')
        self.style.configure('Action.TLabel', font=self.list_font)
        self.style.configure('TButton', font=self.button_font)

        self._create_widgets()

    def _create_widgets(self):
        # Header
        header_frame = ttk.Frame(self, style='Header.TFrame')
        header_frame.pack(fill=tk.X)

        ttk.Label(
            header_frame,
            text="Library Management System",
            style='Header.TLabel',
            font=self.title_font
        ).pack(side=tk.LEFT, padx=20, pady=15)

        user_frame = ttk.Frame(header_frame, style='Header.TFrame')
        user_frame.pack(side=tk.RIGHT, padx=20)

        ttk.Label(
            user_frame,
            text=f"Welcome, {self.user.full_name}",
            style='Header.TLabel',
            font=self.small_font
        ).pack(side=tk.LEFT, padx=5)

        exit_btn = ttk.Button(
            user_frame,
            text="Exit",
            command=self._exit,
            style='TButton'
        )
        exit_btn.pack(side=tk.LEFT, padx=5)

        # Main content frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=30)

        actions = [
            ("👤", "Member Registration", self._open_member_registration),
            ("📚", "Book Management", self._open_book_management),
            ("📖", "Book Lending", self._open_book_lending),
            ("↩️", "Book Returns", self._open_book_returns),
            ("💰", "Fine Calculation", self._open_fine_calculation),
            ("📊", "Inventory Reports", self._open_inventory_reports),
        ]

        for icon, text, command in actions:
            action_frame = tk.Frame(
                main_frame,
                bg="white",
                bd=2,
                relief="solid",
                highlightbackground="gray",
                highlightthickness=1
            )
            action_frame.pack(fill=tk.X, pady=15, ipadx=15, ipady=15)

            label = ttk.Label(
                action_frame,
                text=f"{icon}  {text}",
                style='Action.TLabel',
                background="white"
            )
            label.pack(side=tk.LEFT, padx=20)

            action_btn = ttk.Button(
                action_frame,
                text="Open",
                command=command
            )
            action_btn.pack(side=tk.RIGHT, padx=20)

    def _exit(self):
        AuthService.logout()
        self.destroy()
        self.on_logout()

    def _open_book_management(self):
        BookManagementView(self, self.user)

    def _open_inventory_reports(self):
        InventoryReportsView(self)

    def _open_member_registration(self):
        MemberRegistrationView(self, self.user)

    def _open_book_lending(self):
        BookLendingView(self, self.user)

    def _open_book_returns(self):
        BookReturnView(self)

    def _open_fine_calculation(self):
        FineManagementView(self)
