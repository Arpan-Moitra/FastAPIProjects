from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


# GET request methods
@app.get("/books")
async def read_all_books():
    return BOOKS


# Using Path Parameter
@app.get("/books/{book_title}")
async def read_book(book_title: str):
    for book in BOOKS:
        if book['title'].lower() == book_title.lower():
            return book
    return {"message": "Invalid Book Name"}


# Using Query Parameter
@app.get("/books/")
async def read_book_by_category(category: str):
    category_books = []
    for book in BOOKS:
        if book['category'].lower() == category.lower():
            category_books.append(book)

    return category_books


# Query Parameter
@app.get('/books/by_author/')
async def read_books_by_author_query(author_name: str):
    books_to_be_returned = []
    for book in BOOKS:
        if book['author'].lower() == author_name.lower():
            books_to_be_returned.append(book)

    return books_to_be_returned


# Using both Path and Query Parameters
@app.get("/books/{author_name}/")
async def read_book_by_author_and_category(author_name: str, category: str):
    books_to_be_returned = []
    for book in BOOKS:
        if (book['author'].lower() == author_name.lower()
                and
                book['category'].lower() == category.lower()):
            books_to_be_returned.append(book)

    return books_to_be_returned


# Path Parameter
@app.get('/books/by_author/{author_name}')
async def read_books_by_author_path(author_name: str):
    books_to_be_returned = []
    for book in BOOKS:
        if book['author'].lower() == author_name.lower():
            books_to_be_returned.append(book)

    return books_to_be_returned


# POST request Method
@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)


# PUT request Method
@app.put('/books/update_book')
async def update_book(updated_book=Body()):
    for ind, book in enumerate(BOOKS):
        if book['title'].lower() == updated_book['title'].lower():
            BOOKS[ind] = updated_book


# DELETE request Method
@app.delete('/books/delete_book/{book_title}')
async def delete_book(book_title: str):
    for ind, book in enumerate(BOOKS):
        if book['title'].lower() == book_title.lower():
            BOOKS.pop(ind)

    return BOOKS
