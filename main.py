print("Library Management")

import sqlite3

#options
user_options = input("Choose an option\n"
                     "1. Add new book\n"
                     "2. List books\n"
                     "3. Delete book\n"
                     "4. Search book\n"
                     ":")


def connect_to_database():
    # Connect to a database (creates it if it doesn't exist)
    return sqlite3.connect('books.db')

def create_books_table(cursor):
    # Execute a SQL command to create a table with time_added column
    cursor.execute('''CREATE TABLE IF NOT EXISTS books
                       (id INTEGER PRIMARY KEY, 
                       book_name TEXT, 
                       book_no INTEGER, 
                       time_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

def book_exists(cursor, book_name):
    # Check if a book with the same name (case-insensitive) already exists
    cursor.execute("SELECT * FROM books WHERE LOWER(book_name) = LOWER(?)", (book_name,))
    return cursor.fetchone() is not None

def add_new_book():
    # Get user input
    book_name = input("Enter book name: ")
    book_no = input("Enter book no: ")

    # Connect to the database
    with connect_to_database() as conn:
        # Create a cursor object
        cursor = conn.cursor()

        # Create the books table if it doesn't exist
        create_books_table(cursor)

        # Check if a book with the same name already exists
        existing_book = book_exists(cursor, book_name)

        if existing_book:
            # Book with the same name already exists
            overwrite = input("A book with the same name already exists. Do you want to overwrite it? (yes/no): ").lower()

            if overwrite == 'yes':
                # Overwrite the existing record
                cursor.execute("DELETE FROM books WHERE LOWER(book_name) = LOWER(?)", (book_name,))
                print("Existing record overwritten.")

                # Insert the new data
                cursor.execute("INSERT INTO books (book_name, book_no) VALUES (?, ?)", (book_name, book_no))
                print("New book added.")
            else:
                print("New book not added.")
        else:
            # Book with the same name doesn't exist, proceed with adding the new book
            cursor.execute("INSERT INTO books (book_name, book_no) VALUES (?, ?)", (book_name, book_no))
            print("New book added.")

def list_books():
    # Connect to the database
    with connect_to_database() as conn:
        # Create a cursor object
        cursor = conn.cursor()

        # Create the books table if it doesn't exist
        create_books_table(cursor)

        # Query data from the books table
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()

        # Display the results
        if books:
            print("List of Books:")
            for book in books:
                print(f"ID: {book[0]}, Name: {book[1]}, Book No: {book[2]}, Time Added: {book[3]}")
        else:
            print("No books found.")


def delete_book():
    # Get user input for the book ID to delete
    book_id_to_delete = input("Enter the ID of the book you want to delete: ")

    # Connect to the database
    with connect_to_database() as conn:
        # Create a cursor object
        cursor = conn.cursor()

        # Create the books table if it doesn't exist
        create_books_table(cursor)

        # Check if the book with the given ID exists
        cursor.execute("SELECT * FROM books WHERE id = ?", (book_id_to_delete,))
        book_to_delete = cursor.fetchone()

        if book_to_delete:
            # Delete the book with the specified ID
            cursor.execute("DELETE FROM books WHERE id = ?", (book_id_to_delete,))
            print(f"Book with ID {book_id_to_delete} deleted.")
        else:
            print(f"No book found with ID {book_id_to_delete}.")

def search_books():
    # Get user input for the search term
    search_term = input("Enter a search term (part of the book name): ")

    # Connect to the database
    with connect_to_database() as conn:
        # Create a cursor object
        cursor = conn.cursor()

        # Create the books table if it doesn't exist
        create_books_table(cursor)

        # Query data from the books table based on the search term
        cursor.execute("SELECT * FROM books WHERE book_name LIKE ?", ('%' + search_term + '%',))
        found_books = cursor.fetchall()

        # Display the results
        if found_books:
            print("Found Books:")
            for book in found_books:
                print(f"ID: {book[0]}, Name: {book[1]}, Book No: {book[2]}, Time Added: {book[3]}")
        else:
            print("No books found with the specified search term.")

# Define a dictionary to map options to functions
options_dict = {
    '1': add_new_book,
    '2': list_books,
    '3': delete_book,
    '4': search_books
}

# Get the function associated with the chosen option and call it
selected_option = options_dict.get(user_options)
if selected_option:
    selected_option()
else:
    print("Invalid option")