# app/models/user.py
class User:
    def __init__(self, user_id=None, username=None, password=None, full_name=None, email=None, role=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.full_name = full_name
        self.email = email
        self.role = role

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role
        }