# app/main.py
import tkinter as tk
from app.views.login_view import LoginView
from app.views.admin_panel_view import AdminPanelView
from app.database.db_handler import db


class LibraryManagementSystem:
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # Hide the root window

        self.current_user = None
        self.admin_panel = None

        self._show_login()

    def _show_login(self):
        LoginView(self.root, self._on_login_success)

    def _on_login_success(self, user):
        self.current_user = user
        self.admin_panel = AdminPanelView(user, self._on_logout)

    def _on_logout(self):
        if self.admin_panel:
            self.admin_panel.destroy()
        self.current_user = None
        self._show_login()

    def run(self):
        self.root.mainloop()
        db.close()


if __name__ == "__main__":
    app = LibraryManagementSystem()
    app.run()