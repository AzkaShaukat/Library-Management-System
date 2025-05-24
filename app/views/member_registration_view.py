# member_registration_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from app.services.member_service import MemberService
from app.services.user_service import UserService


class MemberRegistrationView(tk.Toplevel):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("👤 Member Management")
        self.geometry("1200x750")
        self.minsize(1000, 600)

        # Theme
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
        self.border_color = '#d1d8de'

        # Fonts
        self.font_family = "Segoe UI"
        self.font_normal = (self.font_family, 10)
        self.font_bold = (self.font_family, 10, "bold")
        self.font_title_section = (self.font_family, 16, "bold")
        self.font_treeview_heading = (self.font_family, 10, "bold")
        self.font_treeview_row = (self.font_family, 10)
        self.font_button = (self.font_family, 10, "bold")

        self.configure(bg=self.bg_color)
        self._setup_styles()
        self._create_widgets()
        self._load_members()
        self.grab_set()

    def _setup_styles(self):
        style = ttk.Style(self)
        style.theme_use('clam')
        style.configure('TFrame', background=self.bg_color)
        style.configure('Card.TFrame', background=self.fg_color)
        style.configure('TLabel', background=self.bg_color, foreground=self.text_color, font=self.font_normal)
        style.configure('Header.TLabel', background=self.bg_color, foreground=self.header_bg_color, font=self.font_title_section)

        style.configure('Treeview', font=self.font_treeview_row, rowheight=30,
                        fieldbackground=self.fg_color, background=self.fg_color)
        style.configure('Treeview.Heading', font=self.font_treeview_heading,
                        background=self.header_bg_color, foreground=self.header_fg_color)
        style.map('Treeview.Heading', background=[('active', self.primary_color)])

        style.configure('TButton', font=self.font_button, padding=8)
        style.configure('Primary.TButton', background=self.primary_color, foreground='white')
        style.map('Primary.TButton', background=[('active', self.primary_dark_color)])
        style.configure('Success.TButton', background=self.success_color, foreground='white')
        style.map('Success.TButton', background=[('active', self.success_dark_color)])
        style.configure('Danger.TButton', background=self.danger_color, foreground='white')
        style.map('Danger.TButton', background=[('active', self.danger_dark_color)])

    def _create_widgets(self):
        outer_frame = ttk.Frame(self, padding=20)
        outer_frame.pack(fill=tk.BOTH, expand=True)

        header_frame = ttk.Frame(outer_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        ttk.Label(header_frame, text="Member Management", style='Header.TLabel').pack(side=tk.LEFT)

        content_card = ttk.Frame(outer_frame, style='Card.TFrame', padding=20)
        content_card.pack(fill=tk.BOTH, expand=True)
        content_card.configure(relief="solid", borderwidth=1)

        # Search
        search_frame = ttk.Frame(content_card, style='Card.TFrame')
        search_frame.pack(fill=tk.X, pady=(0, 15))

        ttk.Label(search_frame, text="🔍", font=(self.font_family, 12), background=self.fg_color).pack(side=tk.LEFT, padx=(0, 8))
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0,10))
        self.search_entry.bind('<KeyRelease>', self._search_members)

        # Treeview
        tree_frame = ttk.Frame(content_card, style='Card.TFrame')
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=(0,15))

        columns = ["ID", "Name", "CNIC", "Phone", "Email", "City", "Status"]
        self.member_tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, anchor="w", width=130)

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.member_tree.yview)
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.member_tree.pack(side="left", fill=tk.BOTH, expand=True)

        # Buttons
        button_frame = ttk.Frame(content_card, style='Card.TFrame')
        button_frame.pack(fill=tk.X, pady=(10, 0))

        for text, cmd, style in [
            ("➕ Add New", self._open_add_dialog, 'Success.TButton'),
            ("✏️ Update", self._open_update_dialog, 'Primary.TButton'),
            ("🗑️ Delete", self._delete_member, 'Danger.TButton'),
            ("ℹ️ Details", self._view_member_details, 'TButton')
        ]:
            ttk.Button(button_frame, text=text, command=cmd, style=style).pack(side=tk.LEFT, padx=(0, 10))

    def _load_members(self, search_term=None):
        for row in self.member_tree.get_children():
            self.member_tree.delete(row)
        members = MemberService.search_members(search_term) if search_term else MemberService.get_all_members()
        for m in members:
            self.member_tree.insert('', 'end', values=(
                m.member_id, f"{m.first_name} {m.last_name}", m.cnic or "N/A",
                m.phone, m.email or "N/A", m.city or "N/A", m.membership_status.capitalize()))

    def _search_members(self, event=None):
        self._load_members(self.search_entry.get().strip())

    def _open_add_dialog(self):
        self._member_dialog("Add New Member", self._save_new_member)

    def _open_update_dialog(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member to update", parent=self)
            return
        member_id = self.member_tree.item(selected[0])['values'][0]
        member = MemberService.get_member_by_id(member_id)
        if member:
            self._member_dialog("Update Member", self._save_updated_member, member)

    def _view_member_details(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member", parent=self)
            return
        member_id = self.member_tree.item(selected[0])['values'][0]
        m = MemberService.get_member_by_id(member_id)
        if m:
            info = (
                f"ID: {m.member_id}\nName: {m.first_name} {m.last_name}\n"
                f"Phone: {m.phone}\nEmail: {m.email or 'N/A'}\n"
                f"Address: {m.address or 'N/A'}\nCity: {m.city or 'N/A'}\n"
                f"Status: {m.membership_status.capitalize()}"
            )
            messagebox.showinfo("Member Details", info, parent=self)

    def _member_dialog(self, title, save_callback, member=None):
        dialog = tk.Toplevel(self)
        dialog.title(title)
        dialog.geometry("450x500")
        dialog.configure(bg=self.fg_color)
        dialog.grab_set()

        frame = ttk.Frame(dialog, padding=20, style='Card.TFrame')
        frame.pack(fill=tk.BOTH, expand=True)

        fields = [
            ("first_name", "First Name *"), ("last_name", "Last Name *"),
            ("cnic", "CNIC"), ("phone", "Phone *"), ("email", "Email"),
            ("address", "Address"), ("city", "City"), ("membership_status", "Status")
        ]
        entries = {}
        for i, (key, label) in enumerate(fields):
            ttk.Label(frame, text=label, style='TLabel').grid(row=i, column=0, sticky='w', pady=5)
            entry = ttk.Entry(frame, width=35)
            entry.grid(row=i, column=1, pady=5)
            entries[key] = entry
            if member and hasattr(member, key):
                val = getattr(member, key)
                entry.insert(0, str(val) if val is not None else "")

        if member:
            entries["member_id"] = member.member_id

        btn_frame = ttk.Frame(frame, style='Card.TFrame')
        btn_frame.grid(row=len(fields), column=0, columnspan=2, pady=(20, 0), sticky="e")

        ttk.Button(btn_frame, text="Save", style="Success.TButton",
                   command=lambda: save_callback(dialog, entries)).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", style="TButton", command=dialog.destroy).pack(side=tk.LEFT)

    def _save_new_member(self, window, entries):
        data = {k: e.get().strip() for k, e in entries.items()}
        data['added_by'] = self.current_user.user_id
        if not data["first_name"] or not data["last_name"] or not data["phone"]:
            messagebox.showerror("Missing Info", "First Name, Last Name and Phone are required.", parent=window)
            return
        if MemberService.add_member(data):
            window.destroy()
            self._load_members()
            messagebox.showinfo("Success", "Member added successfully.", parent=self)
        else:
            messagebox.showerror("Error", "Failed to add member. CNIC may already exist.", parent=window)

    def _save_updated_member(self, window, entries):
        data = {k: e.get().strip() for k, e in entries.items()}
        if not data["first_name"] or not data["last_name"] or not data["phone"]:
            messagebox.showerror("Missing Info", "First Name, Last Name and Phone are required.", parent=window)
            return
        if MemberService.update_member(data):
            window.destroy()
            self._load_members()
            messagebox.showinfo("Success", "Member updated successfully.", parent=self)
        else:
            messagebox.showerror("Error", "Failed to update member.", parent=window)

    def _delete_member(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("No Selection", "Please select a member to delete.", parent=self)
            return
        member_id = self.member_tree.item(selected[0])['values'][0]
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this member?", parent=self):
            if MemberService.delete_member(member_id):
                self._load_members()
                messagebox.showinfo("Deleted", "Member deleted successfully.", parent=self)
            else:
                messagebox.showerror("Error", "Could not delete member.", parent=self)
