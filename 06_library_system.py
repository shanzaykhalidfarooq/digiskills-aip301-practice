#Library & Book Borrowing Management System
class LibraryError(Exception):
    """Base exception class for library operations."""
    pass

class BookNotFoundError(LibraryError):
    """Raised when a requested book ISBN does not exist."""
    pass

class BookAlreadyBorrowedError(LibraryError):
    """Raised when attempting to borrow an unavailable book."""
    pass

class UserNotFoundError(LibraryError):
    """Raised when a user ID is not registered."""
    pass


class Book:
    def __init__(self, title: str, author: str, isbn: int):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._is_borrowed = False

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string.")
        self._title = value

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Author must be a non-empty string.")
        self._author = value

    @property
    def isbn(self):
        return self._isbn

    @property
    def is_borrowed(self):
        return self._is_borrowed

    @is_borrowed.setter
    def is_borrowed(self, status: bool):
        if not isinstance(status, bool):
            raise ValueError("Borrow status must be a boolean.")
        self._is_borrowed = status

    def get_details(self):
        status = "Borrowed" if self._is_borrowed else "Available"
        return f"[{status}] Title: {self._title} | Author: {self._author} | ISBN: {self._isbn}"

    def __str__(self):
        return self.get_details()


class EBook(Book):
    def __init__(self, title: str, author: str, isbn: int, file_size_mb: float):
        super().__init__(title, author, isbn)
        self._file_size_mb = file_size_mb

    @property
    def file_size_mb(self):
        return self._file_size_mb

    @file_size_mb.setter
    def file_size_mb(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("File size must be a positive number.")
        self._file_size_mb = value

    def get_details(self):
        base_details = super().get_details()
        return f"{base_details} | File Size: {self._file_size_mb} MB"


class User:
    def __init__(self, name: str, user_id: int):
        self._name = name
        self._user_id = user_id
        self._borrowed_books = []

    @property
    def name(self):
        return self._name

    @property
    def user_id(self):
        return self._user_id

    @property
    def borrowed_books(self):
        return self._borrowed_books

    def borrow_book(self, book: Book):
        if book.is_borrowed:
            raise BookAlreadyBorrowedError(f"'{book.title}' is currently unavailable.")
        book.is_borrowed = True
        self._borrowed_books.append(book)
        print(f"Success: {self._name} borrowed '{book.title}'.")

    def return_book(self, book: Book):
        if book in self._borrowed_books:
            book.is_borrowed = False
            self._borrowed_books.remove(book)
            print(f"Success: {self._name} returned '{book.title}'.")
        else:
            print(f"Notice: {self._name} does not have '{book.title}' checked out.")

    def get_details(self):
        titles = [b.title for b in self._borrowed_books]
        return f"User ID: {self._user_id} | Name: {self._name} | Borrowed: {titles}"


class Library:
    def __init__(self, data_file="catalog.txt"):
        self._books = {}
        self._users = {}
        self.data_file = data_file
        self.load_from_file()

    def add_book(self, book: Book):
        if book.isbn in self._books:
            print(f"Notice: ISBN {book.isbn} already exists.")
            return
        self._books[book.isbn] = book
        self.save_to_file()
        print(f"Success: Added '{book.title}' to the library.")

    def register_user(self, user: User):
        if user.user_id in self._users:
            print(f"Notice: User ID {user.user_id} is already registered.")
            return
        self._users[user.user_id] = user
        print(f"Success: Registered user '{user.name}'.")

    def borrow_book_transaction(self, user_id: int, isbn: int):
        if user_id not in self._users:
            raise UserNotFoundError(f"User ID {user_id} not found.")
        if isbn not in self._books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")
        
        user = self._users[user_id]
        book = self._books[isbn]
        user.borrow_book(book)
        self.save_to_file()

    def return_book_transaction(self, user_id: int, isbn: int):
        if user_id not in self._users:
            raise UserNotFoundError(f"User ID {user_id} not found.")
        if isbn not in self._books:
            raise BookNotFoundError(f"Book with ISBN {isbn} not found.")

        user = self._users[user_id]
        book = self._books[isbn]
        user.return_book(book)
        self.save_to_file()

    def list_books(self):
        if not self._books:
            print("No books available in the library.")
            return
        print("\n--- Library Catalog ---")
        for book in self._books.values():
            print(book)

    def list_users(self):
        if not self._users:
            print("No users registered.")
            return
        print("\n--- Registered Users ---")
        for user in self._users.values():
            print(user.get_details())

    def save_to_file(self):
        try:
            with open(self.data_file, "w") as f:
                for book in self._books.values():
                    b_type = "EBook" if isinstance(book, EBook) else "Book"
                    size = getattr(book, "file_size_mb", 0.0)
                    f.write(f"{b_type}|{book.title}|{book.author}|{book.isbn}|{book.is_borrowed}|{size}\n")
        except IOError as e:
            print(f"Error saving data to file: {e}")

    def load_from_file(self):
        try:
            with open(self.data_file, "r") as f:
                for line in f:
                    data = line.strip().split("|")
                    if len(data) == 6:
                        b_type, title, author, isbn, is_borrowed, size = data
                        isbn = int(isbn)
                        is_borrowed = is_borrowed == "True"
                        
                        if b_type == "EBook":
                            book = EBook(title, author, isbn, float(size))
                        else:
                            book = Book(title, author, isbn)
                        
                        book.is_borrowed = is_borrowed
                        self._books[isbn] = book
        except FileNotFoundError:
            pass
        except Exception as e:
            print(f"Error loading file data: {e}")


def main():
    library = Library()

    while True:
        print("\n==========================================")
        print(" LIBRARY & BOOK MANAGEMENT SYSTEM")
        print("==========================================")
        print("1. Add Physical Book")
        print("2. Add EBook")
        print("3. Register User")
        print("4. Borrow Book")
        print("5. Return Book")
        print("6. List All Books")
        print("7. List All Users")
        print("8. Exit")

        choice = input("\nEnter your choice (1-8): ").strip()

        try:
            if choice == "1":
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                isbn = int(input("Enter ISBN (Numbers only): "))
                library.add_book(Book(title, author, isbn))

            elif choice == "2":
                title = input("Enter Title: ")
                author = input("Enter Author: ")
                isbn = int(input("Enter ISBN (Numbers only): "))
                size = float(input("Enter File Size (MB): "))
                library.add_book(EBook(title, author, isbn, size))

            elif choice == "3":
                name = input("Enter User Name: ")
                user_id = int(input("Enter User ID (Numbers only): "))
                library.register_user(User(name, user_id))

            elif choice == "4":
                user_id = int(input("Enter User ID: "))
                isbn = int(input("Enter Book ISBN: "))
                library.borrow_book_transaction(user_id, isbn)

            elif choice == "5":
                user_id = int(input("Enter User ID: "))
                isbn = int(input("Enter Book ISBN: "))
                library.return_book_transaction(user_id, isbn)

            elif choice == "6":
                library.list_books()

            elif choice == "7":
                library.list_users()

            elif choice == "8":
                print("Exiting application. Goodbye!")
                break

            else:
                print("Invalid menu selection. Please enter a number from 1 to 8.")

        except ValueError as ve:
            print(f"Input Error: Please enter valid format data. Details: {ve}")
        except LibraryError as le:
            print(f"Library Error: {le}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()