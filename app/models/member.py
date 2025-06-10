class Member:
    def __init__(self, member_id=None, first_name=None, last_name=None, cnic=None,
                 email=None, phone=None, address=None, city=None,
                 registration_date=None, membership_status='active', registered_by=None):
        self.member_id = member_id
        self.first_name = first_name
        self.last_name = last_name
        self.cnic = cnic
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.registration_date = registration_date
        self.membership_status = membership_status
        self.registered_by = registered_by

    def to_dict(self):
        return {
            'member_id': self.member_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': f"{self.first_name} {self.last_name}",
            'cnic': self.cnic,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'registration_date': self.registration_date,
            'membership_status': self.membership_status,
            'registered_by': self.registered_by
        }

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"