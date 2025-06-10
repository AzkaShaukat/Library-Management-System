from app.models.book import Book #
from app.database.db_handler import db #


class BookService:
    @staticmethod
    def add_book(book_data): #
        # Check for existing ISBN
        existing = db.execute_query("SELECT * FROM books WHERE isbn = %s", (book_data['isbn'],), fetch=True) #
        if existing: #
            return False

        query = """
            INSERT INTO books
            (isbn, title, author, publisher, publication_year, category,
            total_copies, available_copies, shelf_location, added_by)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """ #
        values = ( #
            book_data['isbn'], book_data['title'], book_data['author'],
            book_data.get('publisher'), book_data.get('publication_year'),
            book_data.get('category'), book_data['total_copies'],
            book_data['available_copies'], book_data.get('shelf_location'),
            book_data['added_by']
        )
        return db.execute_query(query, values) #

    @staticmethod
    def update_book(book_data): #
        query = """
            UPDATE books SET
            isbn = %s,
            title = %s,
            author = %s,
            publisher = %s,
            publication_year = %s,
            category = %s,
            total_copies = %s,
            available_copies = %s,
            shelf_location = %s
            WHERE book_id = %s
        """ #
        values = ( #
            book_data['isbn'], book_data['title'], book_data['author'],
            book_data.get('publisher'), book_data.get('publication_year'),
            book_data.get('category'), book_data['total_copies'],
            book_data['available_copies'], book_data.get('shelf_location'),
            book_data['book_id']
        )
        return db.execute_query(query, values) #

    @staticmethod
    def get_all_books(): #
        query = "SELECT * FROM books ORDER BY title" #
        results = db.execute_query(query, fetch=True) #
        return [Book(**row) for row in results] if results else [] #

    @staticmethod
    def get_book_by_id(book_id): #
        query = "SELECT * FROM books WHERE book_id = %s" #
        result = db.execute_query(query, (book_id,), fetch=True) #
        return Book(**result[0]) if result else None #

    @staticmethod
    def delete_book(book_id): #
        query = "DELETE FROM books WHERE book_id = %s" #
        return db.execute_query(query, (book_id,)) #

    @staticmethod
    def get_available_books():
        query = "SELECT * FROM books WHERE available_copies > 0 ORDER BY title"
        results = db.execute_query(query, fetch=True)
        return [Book(**row) for row in results] if results else []
