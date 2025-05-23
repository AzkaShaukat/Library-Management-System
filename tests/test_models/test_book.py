import unittest
from app.models.book import Book

class TestBookModel(unittest.TestCase):
    def test_book_creation(self):
        book = Book(1, '123456', 'Test Book', 'Author Name', 'Publisher', 2020,
                    'Fiction', 10, 9, 'Shelf1', 1)
        self.assertEqual(book.title, 'Test Book')
        self.assertEqual(book.available_copies, 9)

if __name__ == '__main__':
    unittest.main()