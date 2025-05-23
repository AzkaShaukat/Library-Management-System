import tkinter as tk
from tkinter import ttk, messagebox
from app.services.member_service import MemberService
from app.services.user_service import UserService


class MemberRegistrationView(tk.Toplevel):
    def __init__(self, parent, current_user):
        super().__init__(parent)
        self.current_user = current_user
        self.title("Member Registration")
        self.geometry("800x600")
        self.resizable(False, False)

        self._setup_styles()
        self._create_widgets()
        self._load_members()

    def _setup_styles(self):
        self.style = ttk.Style()
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', font=('Helvetica', 10))
        self.style.configure('Header.TLabel', font=('Helvetica', 12, 'bold'))
        self.style.configure('Treeview', font=('Helvetica', 10))
        self.style.configure('Treeview.Heading', font=('Helvetica', 10, 'bold'))
        self.style.configure('TButton', font=('Helvetica', 10))

    def _create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Search frame
        search_frame = ttk.Frame(main_frame)
        search_frame.pack(fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=30)
        self.search_entry.pack(side=tk.LEFT, padx=5)
        self.search_entry.bind('<KeyRelease>', self._search_members)

        ttk.Button(
            search_frame,
            text="🔍 Search",
            command=self._search_members
        ).pack(side=tk.LEFT, padx=5)

        # Treeview for member list
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        columns = [
            ("ID", 50), ("Name", 150), ("CNIC", 120),
            ("Phone", 120), ("City", 100), ("Status", 80)
        ]

        self.member_tree = ttk.Treeview(
            tree_frame,
            columns=[col[0] for col in columns],
            show="headings",
            selectmode="browse"
        )

        for col, width in columns:
            self.member_tree.heading(col, text=col)
            self.member_tree.column(col, width=width, anchor="center")

        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.member_tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.member_tree.configure(yscrollcommand=scrollbar.set)
        self.member_tree.pack(fill=tk.BOTH, expand=True)

        # Button frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(
            button_frame,
            text="➕ Add New Member",
            command=self._open_add_dialog,
            style="Accent.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="✏️ Update Selected",
            command=self._open_update_dialog
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="❌ Delete Selected",
            command=self._delete_member,
            style="Danger.TButton"
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="📝 View Details",
            command=self._view_member_details
        ).pack(side=tk.LEFT, padx=5)

    def _load_members(self):
        for row in self.member_tree.get_children():
            self.member_tree.delete(row)

        members = MemberService.get_all_members()
        for member in members:
            self.member_tree.insert('', 'end', values=(
                member.member_id,
                f"{member.first_name} {member.last_name}",
                member.cnic,
                member.phone,
                member.city,
                member.membership_status
            ))

    def _search_members(self, event=None):
        search_term = self.search_entry.get()
        if not search_term:
            self._load_members()
            return

        for row in self.member_tree.get_children():
            self.member_tree.delete(row)

        members = MemberService.search_members(search_term)
        for member in members:
            self.member_tree.insert('', 'end', values=(
                member.member_id,
                f"{member.first_name} {member.last_name}",
                member.cnic,
                member.phone,
                member.city,
                member.membership_status
            ))

    def _open_add_dialog(self):
        self._member_dialog("Add New Member", self._save_new_member)

    def _open_update_dialog(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to update")
            return

        member_id = self.member_tree.item(selected[0])['values'][0]
        member = MemberService.get_member_by_id(member_id)

        if member:
            self._member_dialog("Update Member", self._save_updated_member, member)

    def _view_member_details(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member")
            return

        member_id = self.member_tree.item(selected[0])['values'][0]
        member = MemberService.get_member_by_id(member_id)

        if member:
            details = (
                f"Member ID: {member.member_id}\n"
                f"Name: {member.first_name} {member.last_name}\n"
                f"CNIC: {member.cnic}\n"
                f"Email: {member.email}\n"
                f"Phone: {member.phone}\n"
                f"Address: {member.address}\n"
                f"City: {member.city}\n"
                f"Status: {member.membership_status}\n"
                f"Registered On: {member.registration_date}\n"
                f"Registered By: {UserService.get_user_name(member.registered_by)}"
            )
            messagebox.showinfo("Member Details", details)

    def _member_dialog(self, title, save_command, member=None):
        window = tk.Toplevel(self)
        window.title(title)
        window.resizable(False, False)

        # Error label
        self.error_label = ttk.Label(window, foreground="red")
        self.error_label.grid(row=0, columnspan=2, pady=5)

        fields = [
            "first_name", "last_name", "cnic", "email",
            "phone", "address", "city", "membership_status"
        ]
        entries = {}

        for i, field in enumerate(fields):
            ttk.Label(window, text=field.replace('_', ' ').title() + ":").grid(
                row=i + 1, column=0, sticky="e", padx=5, pady=5)

            if field == "membership_status":
                entry = ttk.Combobox(window, values=["active", "expired", "suspended"])
            else:
                entry = ttk.Entry(window)

            entry.grid(row=i + 1, column=1, padx=5, pady=5, sticky="ew")
            entries[field] = entry

            # Pre-fill for update
            if member and hasattr(member, field):
                entry.insert(0, str(getattr(member, field)))

        # Store member_id for updates
        if member:
            entries['member_id'] = member.member_id

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

    def _save_new_member(self, window, entries):
        member_data = {f: entries[f].get() for f in [
            "first_name", "last_name", "cnic", "email",
            "phone", "address", "city", "membership_status"
        ]}
        member_data['registered_by'] = self.current_user.user_id

        # Validate required fields
        required = ["first_name", "last_name", "phone", "address", "city"]
        if not all(member_data[field] for field in required):
            self.error_label.config(text="Please fill all required fields")
            return

        if MemberService.register_member(member_data):
            window.destroy()
            self._load_members()
            messagebox.showinfo("Success", "Member registered successfully")
        else:
            self.error_label.config(text="Failed to register member")

    def _save_updated_member(self, window, entries):
        member_data = {f: entries[f].get() for f in [
            "first_name", "last_name", "cnic", "email",
            "phone", "address", "city", "membership_status"
        ]}
        member_id = entries['member_id']

        # Validate required fields
        required = ["first_name", "last_name", "phone", "address", "city"]
        if not all(member_data[field] for field in required):
            self.error_label.config(text="Please fill all required fields")
            return

        if MemberService.update_member(member_id, member_data):
            window.destroy()
            self._load_members()
            messagebox.showinfo("Success", "Member updated successfully")
        else:
            self.error_label.config(text="Failed to update member")

    def _delete_member(self):
        selected = self.member_tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a member to delete")
            return

        member_id = self.member_tree.item(selected[0])['values'][0]
        member_name = self.member_tree.item(selected[0])['values'][1]

        if messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete '{member_name}'?\nThis action cannot be undone!",
                icon='warning'
        ):
            if MemberService.delete_member(member_id):
                messagebox.showinfo("Success", "Member deleted successfully")
                self._load_members()
            else:
                messagebox.showerror("Error", "Failed to delete member. Member may have active loans.")