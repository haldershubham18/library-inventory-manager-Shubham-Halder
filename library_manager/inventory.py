import os
import logging
from typing import List, Optional
from .book import Book

class LibraryInventory:
    """Manages the library's book inventory"""
    
    def __init__(self, storage_file="books.txt"):
        self.books = []
        self.storage_file = storage_file
        self.logger = self._setup_logger()
        self.load_from_file()
    
    def _setup_logger(self):
        """Setup logging configuration"""
        logger = logging.getLogger('LibraryInventory')
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def add_book(self, title: str, author: str, isbn: str) -> bool:
        """Add a new book to the inventory"""
        try:
            # Check if ISBN already exists
            if any(book.isbn == isbn for book in self.books):
                self.logger.warning(f"Book with ISBN {isbn} already exists")
                return False
            
            new_book = Book(title, author, isbn)
            self.books.append(new_book)
            self.logger.info(f"Added book: {title} by {author}")
            self.save_to_file()
            return True
        
        except Exception as e:
            self.logger.error(f"Error adding book: {str(e)}")
            return False
    
    def search_by_title(self, title: str) -> List[Book]:
        """Search books by title (case-insensitive partial match)"""
        try:
            title_lower = title.lower()
            return [book for book in self.books if title_lower in book.title.lower()]
        
        except Exception as e:
            self.logger.error(f"Error searching by title: {str(e)}")
            return []
    
    def search_by_isbn(self, isbn: str) -> Optional[Book]:
        """Search book by exact ISBN match"""
        try:
            for book in self.books:
                if book.isbn == isbn:
                    return book
            return None
        
        except Exception as e:
            self.logger.error(f"Error searching by ISBN: {str(e)}")
            return None
    
    def display_all(self) -> List[Book]:
        """Return all books in inventory"""
        return self.books.copy()
    
    def issue_book(self, isbn: str) -> bool:
        """Issue a book by ISBN"""
        try:
            book = self.search_by_isbn(isbn)
            if book and book.issue():
                self.logger.info(f"Issued book: {book.title}")
                self.save_to_file()
                return True
            return False
        
        except Exception as e:
            self.logger.error(f"Error issuing book: {str(e)}")
            return False
    
    def return_book(self, isbn: str) -> bool:
        """Return a book by ISBN"""
        try:
            book = self.search_by_isbn(isbn)
            if book and book.return_book():
                self.logger.info(f"Returned book: {book.title}")
                self.save_to_file()
                return True
            return False
        
        except Exception as e:
            self.logger.error(f"Error returning book: {str(e)}")
            return False
    
    def save_to_file(self) -> bool:
        """Save inventory to text file"""
        try:
            with open(self.storage_file, 'w', encoding='utf-8') as file:
                for book in self.books:
                    book_data = book.to_dict()
                    # Format: title|author|isbn|status
                    line = f"{book_data['title']}|{book_data['author']}|{book_data['isbn']}|{book_data['status']}\n"
                    file.write(line)
            
            self.logger.info(f"Inventory saved to {self.storage_file}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error saving to file: {str(e)}")
            return False
    
    def load_from_file(self) -> bool:
        """Load inventory from text file"""
        try:
            if not os.path.exists(self.storage_file):
                self.logger.warning(f"Storage file {self.storage_file} not found. Starting with empty inventory.")
                return True
            
            self.books = []
            with open(self.storage_file, 'r', encoding='utf-8') as file:
                for line_num, line in enumerate(file, 1):
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        parts = line.split('|')
                        if len(parts) == 4:
                            title, author, isbn, status = parts
                            book = Book(title, author, isbn, status)
                            self.books.append(book)
                        else:
                            self.logger.warning(f"Invalid format in line {line_num}: {line}")
                    
                    except Exception as e:
                        self.logger.error(f"Error parsing line {line_num}: {str(e)}")
                        continue
            
            self.logger.info(f"Loaded {len(self.books)} books from {self.storage_file}")
            return True
        
        except FileNotFoundError:
            self.logger.warning("Storage file not found. Starting with empty inventory.")
            return True
        except Exception as e:
            self.logger.error(f"Error loading from file: {str(e)}")
            return False
