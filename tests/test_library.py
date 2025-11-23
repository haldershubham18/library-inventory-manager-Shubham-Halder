import unittest
import os
import tempfile
from library_manager.book import Book
from library_manager.inventory import LibraryInventory

class TestBook(unittest.TestCase):
    def test_book_creation(self):
        book = Book("Test Book", "Test Author", "1234567890")
        self.assertEqual(book.title, "Test Book")
        self.assertEqual(book.author, "Test Author")
        self.assertEqual(book.isbn, "1234567890")
        self.assertEqual(book.status, "available")
    
    def test_book_issue_return(self):
        book = Book("Test Book", "Test Author", "1234567890")
        
        # Test issuing
        self.assertTrue(book.issue())
        self.assertEqual(book.status, "issued")
        self.assertFalse(book.is_available())
        
        # Test returning
        self.assertTrue(book.return_book())
        self.assertEqual(book.status, "available")
        self.assertTrue(book.is_available())
    
    def test_to_dict(self):
        book = Book("Test Book", "Test Author", "1234567890", "issued")
        book_dict = book.to_dict()
        
        expected = {
            'title': 'Test Book',
            'author': 'Test Author',
            'isbn': '1234567890',
            'status': 'issued'
        }
        self.assertEqual(book_dict, expected)

class TestLibraryInventory(unittest.TestCase):
    def setUp(self):
        # Create temporary file for testing
        self.temp_file = tempfile.mktemp(suffix='.txt')
        self.inventory = LibraryInventory(self.temp_file)
    
    def tearDown(self):
        # Clean up temporary file
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
    
    def test_add_book(self):
        result = self.inventory.add_book("Test Book", "Test Author", "1234567890")
        self.assertTrue(result)
        self.assertEqual(len(self.inventory.books), 1)
    
    def test_duplicate_isbn(self):
        self.inventory.add_book("Book 1", "Author 1", "1234567890")
        result = self.inventory.add_book("Book 2", "Author 2", "1234567890")
        self.assertFalse(result)
        self.assertEqual(len(self.inventory.books), 1)
    
    def test_search_functions(self):
        self.inventory.add_book("Python Programming", "John Doe", "1111111111")
        self.inventory.add_book("Java Programming", "Jane Smith", "2222222222")
        
        # Search by title
        results = self.inventory.search_by_title("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Programming")
        
        # Search by ISBN
        book = self.inventory.search_by_isbn("2222222222")
        self.assertIsNotNone(book)
        self.assertEqual(book.title, "Java Programming")
    
    def test_file_persistence(self):
        # Add books and save
        self.inventory.add_book("Book 1", "Author 1", "1111111111")
        self.inventory.add_book("Book 2", "Author 2", "2222222222")
        self.inventory.save_to_file()
        
        # Create new inventory and load
        new_inventory = LibraryInventory(self.temp_file)
        self.assertEqual(len(new_inventory.books), 2)

if __name__ == '__main__':
    unittest.main()
