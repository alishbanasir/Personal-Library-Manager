
import streamlit as st
import json
import os

data_file = "library.txt"
def load_library():
    if os.path.exists(data_file):
        with open(data_file, "r") as file:
            return json.load(file)
    return []

def save_library(library):
    with open(data_file, "w") as file:
        json.dump(library, file)

def add_book(library):
    title = st.text_input("Enter the title of the Book:")
    author = st.text_input("Enter the author of the Book:")
    year = st.text_input("Enter the year of the Book:")
    genre = st.text_input("Enter the genre of the Book:")
    read = st.checkbox("Have you read the Book?")

    if st.button("Add Book"):
        if title and author and year and genre:
            new_books = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read,
            }

            library.append(new_books)
            save_library(library)
            st.success(f"Book '{title}' added successfully.")
        else:
            st.error("Please fill all fields.")


def remove_book(library):
    title = st.text_input("Enter the title of the book to remove:")
    
    if st.button("Remove Book"):
        initial_length = len(library)
        updated_library = [book for book in library if book["title"].lower() != title.lower()]

        if len(updated_library) < initial_length:
            save_library(updated_library)
            st.success(f"Book '{title}' removed successfully.")
            return updated_library
        else:
            st.warning(f"Book '{title}' not found in the library.")

    return library


def search_library(library):
    search_by = st.selectbox("Search by:", ["title", "author"])
    search_term = st.text_input(f"Enter the {search_by}:")

    if st.button("Search"):
        results = [book for book in library if search_term.lower() in book[search_by].lower()]

        if results:
            for book in results:
                status = "Read" if book["read"] else "Not Read"
                st.info(f"{book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
        else:
            st.warning(f"No book found matching '{search_term}' in the {search_by} field.")


def Display_Book(library):
    if library:
        for book in library:
            status = "Read" if book["read"] else "Not Read"
            st.write(f"📚 {book['title']} by {book['author']} - {book['year']} - {book['genre']} - {status}")
    else:
        st.info("No books in the library.")


def display_statistics(library):
    total_book = len(library)
    read_book = len([book for book in library if book["read"]])
    percentage_read = (read_book / total_book) * 100 if total_book > 0 else 0

    st.metric("📚 Total Books", total_book)
    st.metric("✅ Read Percentage", f"{percentage_read:.2f}%")


def main():
    st.title("📖 Personal Library Manager")
    library = load_library()

    menu = st.sidebar.radio("**📚 Shelf Sanctuary**", [
        "Add Book", 
        "Remove Book", 
        "Search Library", 
        "Display All Books", 
        "Display Statistics"
    ])

    if menu == "Add Book":
        add_book(library)

    elif menu == "Remove Book":
        library = remove_book(library)

    elif menu == "Search Library":
        search_library(library)

    elif menu == "Display All Books":
        Display_Book(library)

    elif menu == "Display Statistics":
        display_statistics(library)

if __name__ == "__main__":
    main()
        
