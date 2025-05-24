# 📚 Library Management System

A full-featured **Library Management System** developed using **Python (Tkinter)** for the GUI and **MySQL (via XAMPP)** for the backend database. This system is designed to assist librarians in efficiently managing library operations including user authentication, book management, member registration, lending and returning of books, fine calculation, and inventory reporting.

---

## 🧩 Project Structure

```text
library_management_system/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── views/
│   │   ├── login_view.py
│   │   ├── admin_panel_view.py
│   │   ├── book_management_view.py
│   │   ├── member_registration_view.py
│   │   ├── book_lending_view.py
│   │   ├── book_return_view.py
│   │   ├── inventory_reports_view.py
│   │   └── fine_calculation_view.py
│   ├── models/
│   │   ├── user.py
│   │   ├── book.py
│   │   ├── member.py
│   │   └── loan.py
│   ├── services/
│   │   ├── auth_service.py
│   │   ├── book_service.py
│   │   ├── member_service.py
│   │   ├── loan_service.py
│   │   ├── fine_service.py
│   │   └── report_service.py
│   ├── database/
│   │   ├── db_handler.py
│   │   └── setup_db.py
│   └── utils/
│       ├── ui_styles.py
│       └── validators.py
├── tests/
│   ├── test_models/
│   │   ├── test_user.py
│   │   ├── test_member.py
│   │   ├── test_book.py
│   │   └── test_loan.py
│   ├── test_services/
│   │   ├── tesr_auth_service.py
│   │   ├── test_book_service.py
│   │   ├── test_loan_service.py
│   │   ├── test_member_service.py
│   │   └── test_report_service.py
├── requirements.txt
└── README.md
```

---

## 🔐 Features Overview

### 1. **Login & Admin Panel**
- Secure login for librarians
- Centralized dashboard for system access

### 2. **Book Management**
- Add, edit, and remove book records
- Manage book inventory and track availability

### 3. **Member Registration**
- Register new library members with contact information
- Generate unique member IDs

### 4. **Book Lending**
- Issue books to members
- Track loan dates and due dates

### 5. **Book Returns**
- Process returns and update availability
- Auto-detect overdue returns

### 6. **Fine Calculation**
- Calculate fines based on return date
- Display and manage outstanding fines

### 7. **Inventory Reports**
- Generate reports on borrowed books, available stock, and more
- Filter by author, title, or availability

---

## 🛠️ Technologies Used

| Technology       | Purpose                       |
|------------------|-------------------------------|
| Python           | Core programming language     |
| Tkinter          | GUI framework                 |
| MySQL (XAMPP)    | Database management system    |
| mysql-connector-python | Python-MySQL connectivity |
| UnitTest         | Testing framework             |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- XAMPP (MySQL server)
- Install dependencies:

```bash
pip install -r requirements.txt
```
## 🧪 Sample Credentials

Use the following credentials to log in:

| Role       | Username      | Password   |
|------------|---------------|------------|
| Admin      | `AzkaShaukat` | `Azka@123` |
| Admin      | `admin`       | `admin123` |
| Librarian  | `librarian1`  | `libpass`  |

