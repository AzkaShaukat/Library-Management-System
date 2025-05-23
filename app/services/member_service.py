from app.database.db_handler import db
from app.models.member import Member

class MemberService:
    @staticmethod
    def register_member(member_data):
        query = """
            INSERT INTO members 
            (first_name, last_name, cnic, email, phone, address, city, registered_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            member_data['first_name'],
            member_data['last_name'],
            member_data.get('cnic'),
            member_data.get('email'),
            member_data['phone'],
            member_data['address'],
            member_data['city'],
            member_data['registered_by']
        )
        return db.execute_query(query, values)

    @staticmethod
    def get_all_members():
        query = "SELECT * FROM members ORDER BY last_name, first_name"
        results = db.execute_query(query, fetch=True)
        return [Member(**row) for row in results] if results else []

    @staticmethod
    def get_member_by_id(member_id):
        query = "SELECT * FROM members WHERE member_id = %s"
        result = db.execute_query(query, (member_id,), fetch=True)
        return Member(**result[0]) if result else None

    @staticmethod
    def search_members(search_term):
        query = """
            SELECT * FROM members 
            WHERE first_name LIKE %s OR last_name LIKE %s OR cnic LIKE %s OR email LIKE %s
            ORDER BY last_name, first_name
        """
        search_pattern = f"%{search_term}%"
        results = db.execute_query(query, (search_pattern, search_pattern, search_pattern, search_pattern), fetch=True)
        return [Member(**row) for row in results] if results else []

    @staticmethod
    def update_member(member_id, member_data):
        query = """
            UPDATE members SET
            first_name = %s,
            last_name = %s,
            cnic = %s,
            email = %s,
            phone = %s,
            address = %s,
            city = %s,
            membership_status = %s
            WHERE member_id = %s
        """
        values = (
            member_data['first_name'],
            member_data['last_name'],
            member_data.get('cnic'),
            member_data.get('email'),
            member_data['phone'],
            member_data['address'],
            member_data['city'],
            member_data.get('membership_status', 'active'),
            member_id
        )
        return db.execute_query(query, values)

    @staticmethod
    def delete_member(member_id):
        query = "DELETE FROM members WHERE member_id = %s"
        return db.execute_query(query, (member_id,))