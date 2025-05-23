import unittest
from app.services.book_service import BookService
from app.database.db_handler import db

class TestBookService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.book_data = {
            'isbn': '00001112233',
            'title': 'Unit Test Book',
            'author': 'Tester',
            'publisher': 'Test House',
            'publication_year': 2023,
            'category': 'Test',
            'total_copies': 3,
            'available_copies': 3,
            'shelf_location': 'U1-01',
            'added_by': 1
        }

    def test_add_and_delete_book(self):
        result = BookService.add_book(self.book_data)
        self.assertTrue(result)
        books = BookService.get_all_books()
        added = [b for b in books if b.isbn == self.book_data['isbn']]
        self.assertTrue(len(added) == 1)
        deleted = BookService.delete_book(added[0].book_id)
        self.assertTrue(deleted)

if __name__ == '__main__':
    unittest.main()

