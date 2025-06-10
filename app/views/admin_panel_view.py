# admin_panel_view.py
import tkinter as tk
from tkinter import ttk, font
from app.services.auth_service import AuthService
from app.views.login_view import LoginView
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

        # Theme Colors
        self.bg_color = '#f0f2f5'
        self.fg_color = '#ffffff'
        self.primary_color = '#3498db'
        self.primary_dark_color = '#2980b9'
        self.header_bg_color = '#2c3e50'
        self.header_fg_color = '#ffffff'
        self.success_color = '#2ecc71'
        self.danger_color = '#e74c3c'
        self.text_color = '#212529'
        self.border_color = '#d1d8de'

        # Fonts
        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_large_bold = (self.font_family, 12, "bold")
        self.font_title = (self.font_family, 20, "bold")
        self.font_button = (self.font_family, 11, "bold")
        self.font_action_text = (self.font_family, 14)
        self.font_action_icon = (self.font_family, 48)

        self.title(f"Library Management System - Admin Panel ({user.full_name})")
        self.geometry("1200x750")
        self.minsize(1000, 700)
        self.configure(bg=self.bg_color)

        self._configure_styles()
        self._create_widgets()

    def _configure_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('Card.TFrame', background=self.fg_color)
        self.style.configure('TLabel', background=self.bg_color,
                             foreground=self.text_color, font=self.font_normal)
        self.style.configure('Header.TLabel', background=self.header_bg_color,
                             foreground=self.header_fg_color, font=self.font_title)
        self.style.configure('Action.TLabel', font=self.font_action_text,
                             background=self.fg_color, foreground=self.text_color)
        self.style.configure('Action.Icon.TLabel', font=self.font_action_icon,
                             background=self.fg_color, foreground=self.primary_color)

        # Button styles
        self.style.configure('TButton', font=self.font_button, padding=10)
        self.style.configure('Primary.TButton', background=self.primary_color,
                             foreground=self.fg_color)
        self.style.map('Primary.TButton',
                       background=[('active', self.primary_dark_color)])
        self.style.configure('Danger.TButton', background=self.danger_color,
                             foreground=self.fg_color)
        self.style.map('Danger.TButton',
                       background=[('active', '#c0392b')])

    def _create_widgets(self):
        # Header frame
        header_frame = ttk.Frame(self, style='Header.TFrame', padding=(20, 15))
        header_frame.pack(fill=tk.X)

        ttk.Label(header_frame, text="Library Management System",
                  style='Header.TLabel').pack(side=tk.LEFT)

        # User info frame
        user_frame = ttk.Frame(header_frame, style='Header.TFrame')
        user_frame.pack(side=tk.RIGHT, padx=20)

        ttk.Label(user_frame, text=f"Welcome, {self.user.full_name}",
                  style='Header.TLabel', font=self.font_large_bold).pack(side=tk.LEFT, padx=10)

        ttk.Button(user_frame, text="Logout", command=self._exit,
                   style='Danger.TButton').pack(side=tk.LEFT)

        # Main content area
        content_frame = ttk.Frame(self)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Create action cards grid (3 columns)
        actions = [
            ("👤", "Member Registration", self._open_member_registration),
            ("📚", "Book Management", self._open_book_management),
            ("📤", "Book Lending", self._open_book_lending),
            ("📥", "Book Returns", self._open_book_returns),
            ("💰", "Fine Management", self._open_fine_calculation),
            ("📊", "Inventory Reports", self._open_inventory_reports)
        ]

        for i, (icon, text, command) in enumerate(actions):
            row, col = divmod(i, 3)  # 3 columns

            card_frame = ttk.Frame(content_frame, style='Card.TFrame',
                                   padding=20, relief='solid', borderwidth=1)
            card_frame.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")

            # Icon
            ttk.Label(card_frame, text=icon, style='Action.Icon.TLabel'
                      ).pack(pady=(0, 10))

            # Action text
            ttk.Label(card_frame, text=text, style='Action.TLabel',
                      font=self.font_large_bold).pack(pady=(0, 15))

            # Action button
            ttk.Button(card_frame, text="Open", command=command,
                       style='Primary.TButton').pack()

            # Configure grid weights
            content_frame.columnconfigure(col, weight=1)
            content_frame.rowconfigure(row, weight=1)

    def _exit(self):
        AuthService.logout()
        self.destroy()
        self.on_logout()
        BookManagementView(self)

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