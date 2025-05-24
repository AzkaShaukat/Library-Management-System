# login_view.py
import tkinter as tk
from tkinter import ttk, font
from app.services.auth_service import AuthService


class LoginView(tk.Toplevel):
    def __init__(self, parent, on_login_success):
        super().__init__(parent)
        self.on_login_success = on_login_success

        # Configure theme colors
        self.bg_color = '#f0f2f5'
        self.primary_color = '#3498db'
        self.text_color = '#212529'
        self.button_text_color = '#ffffff'
        self.error_color = '#e74c3c'
        self.font_family = "Segoe UI"

        self.title("Library Management System - Login")
        self.geometry("450x550")
        self.resizable(False, False)
        self.configure(bg=self.bg_color)

        # Custom fonts
        self.font_normal = (self.font_family, 11)
        self.font_bold = (self.font_family, 11, "bold")
        self.font_large_bold = (self.font_family, 12, "bold")
        self.font_title_login = (self.font_family, 20, "bold")
        self.font_icon_login = ("Segoe UI Symbol", 60)

        self._configure_styles()
        self._create_widgets()
        self.username_entry.focus_set()

        # Center the window
        self.update_idletasks()
        width = self.winfo_width()
        height = self.winfo_height()
        x = (self.winfo_screenwidth() // 2) - (width // 2)
        y = (self.winfo_screenheight() // 2) - (height // 2)
        self.geometry(f'{width}x{height}+{x}+{y}')

    def _configure_styles(self):
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Configure styles
        self.style.configure('TFrame', background=self.bg_color)
        self.style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.font_normal)
        self.style.configure('Title.TLabel', font=self.font_title_login, foreground=self.primary_color)
        self.style.configure('Icon.TLabel', font=self.font_icon_login, foreground=self.primary_color)
        self.style.configure('TEntry', font=self.font_normal, padding=5)
        self.style.configure('TButton', font=self.font_bold, padding=(10, 8))
        self.style.configure('Login.TButton', background=self.primary_color, foreground=self.button_text_color)
        self.style.map('Login.TButton',
                       background=[('active', '#2980b9'), ('!disabled', self.primary_color)],
                       foreground=[('!disabled', self.button_text_color)])
        self.style.configure('Error.TLabel', foreground=self.error_color, font=(self.font_family, 10))

    def _create_widgets(self):
        main_frame = ttk.Frame(self, padding="30 40 30 40")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Icon
        ttk.Label(main_frame, text="📚", style='Icon.TLabel').pack(pady=(0, 15))

        # Title
        ttk.Label(main_frame, text="LIBRARIAN LOGIN", style='Title.TLabel').pack(pady=(0, 25))

        # Username
        ttk.Label(main_frame, text="Username:").pack(anchor='w', pady=(0, 2))
        self.username_entry = ttk.Entry(main_frame, width=35)
        self.username_entry.pack(fill=tk.X, pady=(0, 10))

        # Password
        ttk.Label(main_frame, text="Password:").pack(anchor='w', pady=(0, 2))
        self.password_entry = ttk.Entry(main_frame, show="•", width=35)
        self.password_entry.pack(fill=tk.X, pady=(0, 10))

        # Error label
        self.error_label = ttk.Label(main_frame, text="", style='Error.TLabel')
        self.error_label.pack(pady=(5, 10))

        # Login Button
        login_btn = ttk.Button(
            main_frame,
            text="Login",
            command=self._login,
            style='Login.TButton',
            cursor="hand2"
        )
        login_btn.pack(fill=tk.X, pady=(15, 0), ipady=5)

        # Bind Enter key to login for both entry fields
        self.username_entry.bind('<Return>', lambda event: self.password_entry.focus_set())
        self.password_entry.bind('<Return>', lambda event: self._login())

        # Protocol for closing window
        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username or not password:
            self.error_label.config(text="Please enter both username and password.")
            return

        user = AuthService.login(username, password)

        if user:
            self.error_label.config(text="")
            self.destroy()
            self.on_login_success(user)
        else:
            self.error_label.config(text="Invalid username or password.")
            self.password_entry.delete(0, tk.END)

    def _on_close(self):
        self.destroy()
        if hasattr(self.master, 'destroy_completely'):
            self.master.destroy_completely()
        else:
            self.master.destroy()