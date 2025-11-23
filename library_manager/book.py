class Book:
    """Represents a book in the library inventory"""
    
    def __init__(self, title, author, isbn, status="available"):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.status = status  # "available" or "issued"
    
    def __str__(self):
        return f"'{self.title}' by {self.author} (ISBN: {self.isbn}) - {self.status}"
    
    def to_dict(self):
        """Convert book object to dictionary for serialization"""
        return {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'status': self.status
        }
    
    def issue(self):
        """Mark book as issued"""
        if self.status == "available":
            self.status = "issued"
            return True
        return False
    
    def return_book(self):
        """Mark book as available"""
        if self.status == "issued":
            self.status = "available"
            return True
        return False
    
    def is_available(self):
        """Check if book is available"""
        return self.status == "available"
    
    @classmethod
    def from_dict(cls, data):
        """Create Book object from dictionary"""
        return cls(data['title'], data['author'], data['isbn'], data['status'])
