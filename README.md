# 📚 Library Management System

A desktop application to help librarians manage book inventory using Python and MySQL.

---

## 🚀 Current Features

### ✅ Module 1: Authentication & Admin Panel
- Secure login system with password hashing (bcrypt)
- Role-based access (Admin/Librarian)
- Modern admin dashboard with navigation
- MySQL database integration via XAMPP
- Responsive Tkinter GUI with beautiful styling

### 📖 Module 2: Book Management
- Add/Edit/Delete books with full details
- ISBN validation and duplicate prevention
- Inventory tracking (total/available copies)
- Advanced search and filtering

### 👥 Module 3: Member Management & Lending
- Member registration system
- Book lending with due dates
- Active loans tracking
- Instant member search functionality
- Automatic availability updates

### 👥 Module 4: Book Returns & Fine Management
- loned book display
- Return processing
- Active loans tracking
- Automatic fine calculation for overdue books
- Fine payment tracking
---
## Technology Stack

- **Frontend**: Tkinter (Python GUI)
- **Backend**: Python 3.9+
- **Database**: MySQL
- **Architecture**: MVC Pattern

## Installation

1. **Prerequisites**:
   - Python 3.9 or later
   - MySQL Server
   - XAMPP (recommended for easy MySQL setup)

2. **Setup Database**:
   - Create a MySQL database named `library_management`
   - Run the SQL script from `database/setup_db.sql`

3. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt