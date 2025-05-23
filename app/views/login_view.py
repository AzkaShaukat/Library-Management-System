# app/views/login_view.py
import tkinter as tk
from tkinter import ttk, font
from app.services.auth_service import AuthService


class LoginView(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success

        self.title("Library Management System - Login")
        self.geometry("1200x700")
        self.minsize(1200, 700)
        self.resizable(False, False)

        # Custom font
        self.custom_font = font.Font(family="Helvetica", size=14)
        self.title_font = font.Font(family="Helvetica", size=20, weight="bold")

        # Configure style
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=self.custom_font)
        self.style.configure('TButton', font=self.custom_font)
        self.style.configure('Error.TLabel', foreground='red', background='#f0f0f0')

        self._create_widgets()

    def _create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title
        ttk.Label(
            main_frame,
            text="LIBRARY MANAGEMENT SYSTEM",
            font=self.title_font
        ).pack(pady=(0, 20))

        # Logo placeholder (you can replace with actual image)
        ttk.Label(
            main_frame,
            text="📚",
            font=("Arial", 100),
            background='#f0f0f0'
        ).pack(pady=(0, 20))

        # Username
        ttk.Label(main_frame, text="Username:").pack()
        self.username_entry = ttk.Entry(main_frame, font=self.custom_font, width=50)
        self.username_entry.pack(pady=5, ipady=5)

        # Password
        ttk.Label(main_frame, text="Password:").pack()
        self.password_entry = ttk.Entry(main_frame, show="•", font=self.custom_font, width=50)
        self.password_entry.pack(pady=5, ipady=5)

        # Error label
        self.error_label = ttk.Label(
            main_frame,
            text="",
            style='Error.TLabel'
        )
        self.error_label.pack()

        # Login Button
        login_btn = ttk.Button(
            main_frame,
            text="Login",
            command=self._login,
            style='TButton'
        )
        login_btn.pack(pady=20, ipady=5, ipadx=20)

        # Bind Enter key to login
        self.password_entry.bind('<Return>', lambda event: self._login())

    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.config(text="Please enter both username and password")
            return

        user = AuthService.login(username, password)

        if user:
            self.error_label.config(text="")
            self.destroy()
            self.on_login_success(user)  # This will now directly open admin panel
        else:
            self.error_label.config(text="Invalid username or password")