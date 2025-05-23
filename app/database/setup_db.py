# Add these to your existing setup_db.py

def create_members_table():
    query = """
    CREATE TABLE IF NOT EXISTS members (
        member_id INT AUTO_INCREMENT PRIMARY KEY,
        first_name VARCHAR(50) NOT NULL,
        last_name VARCHAR(50) NOT NULL,
        email VARCHAR(100) UNIQUE,
        phone VARCHAR(20) NOT NULL,
        address TEXT NOT NULL,
        registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        membership_status ENUM('active', 'expired', 'suspended') DEFAULT 'active',
        registered_by INT,
        FOREIGN KEY (registered_by) REFERENCES users(user_id)
    )
    """
    db.execute_query(query)

def create_loans_table():
    query = """
    CREATE TABLE IF NOT EXISTS loans (
        loan_id INT AUTO_INCREMENT PRIMARY KEY,
        book_id INT NOT NULL,
        member_id INT NOT NULL,
        issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        due_date DATE NOT NULL,
        return_date DATE NULL,
        status ENUM('issued', 'returned', 'overdue') DEFAULT 'issued',
        issued_by INT NOT NULL,
        FOREIGN KEY (book_id) REFERENCES books(book_id),
        FOREIGN KEY (member_id) REFERENCES members(member_id),
        FOREIGN KEY (issued_by) REFERENCES users(user_id)
    )
    """
    db.execute_query(query)

def initialize_module3_tables():
    create_members_table()
    create_loans_table()