import sys
import os
import logging

# Add parent directory to path to import library_manager
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from library_manager.inventory import LibraryInventory

class LibraryCLI:
    """Command Line Interface for Library Inventory Manager"""
    
    def __init__(self):
        self.inventory = LibraryInventory()
        self.setup_logging()
    
    def setup_logging(self):
        """Setup logging configuration"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("      LIBRARY INVENTORY MANAGER")
        print("="*50)
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search by Title")
        print("6. Search by ISBN")
        print("7. Exit")
        print("="*50)
    
    def get_input(self, prompt, validator=None):
        """Get validated input from user"""
        while True:
            try:
                value = input(prompt).strip()
                if validator:
                    if validator(value):
                        return value
                    else:
                        print("Invalid input. Please try again.")
                else:
                    return value
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                return None
            except Exception as e:
                print(f"Input error: {str(e)}")
    
    def validate_not_empty(self, value):
        """Validate that input is not empty"""
        return len(value) > 0
    
    def validate_isbn(self, isbn):
        """Basic ISBN validation"""
        return len(isbn) >= 10 and isbn.replace('-', '').replace(' ', '').isalnum()
    
    def add_book(self):
        """Handle adding a new book"""
        print("\n--- ADD NEW BOOK ---")
        
        title = self.get_input("Enter book title: ", self.validate_not_empty)
        if title is None:
            return
        
        author = self.get_input("Enter author: ", self.validate_not_empty)
        if author is None:
            return
        
        isbn = self.get_input("Enter ISBN: ", self.validate_isbn)
        if isbn is None:
            return
        
        if self.inventory.add_book(title, author, isbn):
            print("✓ Book added successfully!")
        else:
            print("✗ Failed to add book. ISBN might already exist.")
    
    def issue_book(self):
        """Handle issuing a book"""
        print("\n--- ISSUE BOOK ---")
        
        isbn = self.get_input("Enter ISBN of book to issue: ")
        if isbn is None:
            return
        
        if self.inventory.issue_book(isbn):
            print("✓ Book issued successfully!")
        else:
            print("✗ Failed to issue book. Book might not be available or ISBN not found.")
    
    def return_book(self):
        """Handle returning a book"""
        print("\n--- RETURN BOOK ---")
        
        isbn = self.get_input("Enter ISBN of book to return: ")
        if isbn is None:
            return
        
        if self.inventory.return_book(isbn):
            print("✓ Book returned successfully!")
        else:
            print("✗ Failed to return book. Book might not be issued or ISBN not found.")
    
    def view_all_books(self):
        """Display all books"""
        print("\n--- ALL BOOKS ---")
        
        books = self.inventory.display_all()
        if not books:
            print("No books in inventory.")
            return
        
        for i, book in enumerate(books, 1):
            status_icon = "✓" if book.is_available() else "✗"
            print(f"{i}. {status_icon} {book}")
    
    def search_by_title(self):
        """Search books by title"""
        print("\n--- SEARCH BY TITLE ---")
        
        title = self.get_input("Enter title to search: ")
        if title is None:
            return
        
        results = self.inventory.search_by_title(title)
        if not results:
            print("No books found with that title.")
            return
        
        print(f"Found {len(results)} book(s):")
        for i, book in enumerate(results, 1):
            status_icon = "✓" if book.is_available() else "✗"
            print(f"{i}. {status_icon} {book}")
    
    def search_by_isbn(self):
        """Search book by ISBN"""
        print("\n--- SEARCH BY ISBN ---")
        
        isbn = self.get_input("Enter ISBN to search: ")
        if isbn is None:
            return
        
        book = self.inventory.search_by_isbn(isbn)
        if book:
            status_icon = "✓" if book.is_available() else "✗"
            print(f"Found: {status_icon} {book}")
        else:
            print("No book found with that ISBN.")
    
    def run(self):
        """Main CLI loop"""
        print("Welcome to Library Inventory Manager!")
        
        while True:
            self.display_menu()
            choice = self.get_input("\nEnter your choice (1-7): ")
            
            if choice is None:
                break
            
            try:
                if choice == '1':
                    self.add_book()
                elif choice == '2':
                    self.issue_book()
                elif choice == '3':
                    self.return_book()
                elif choice == '4':
                    self.view_all_books()
                elif choice == '5':
                    self.search_by_title()
                elif choice == '6':
                    self.search_by_isbn()
                elif choice == '7':
                    print("Thank you for using Library Inventory Manager!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1-7.")
            
            except Exception as e:
                logging.error(f"Unexpected error: {str(e)}")
                print("An unexpected error occurred. Please try again.")

def main():
    """Main entry point"""
    try:
        cli = LibraryCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\n\nProgram interrupted by user. Goodbye!")
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
