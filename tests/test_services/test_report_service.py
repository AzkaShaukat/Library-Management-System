import unittest
from app.services.report_service import ReportService

class TestReportService(unittest.TestCase):
    def test_get_all_books(self):
        books = ReportService.get_all_books()
        self.assertIsInstance(books, list)

    def test_get_available_books(self):
        available = ReportService.get_available_books()
        self.assertIsInstance(available, list)

if __name__ == '__main__':
    unittest.main()