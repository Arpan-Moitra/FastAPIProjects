from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    book_id: int
    title: str
    author: str
    description: str
    rating: float
    published_date: int

    def __init__(self, book_id, title, author, description, rating, published_date):
        self.title = title
        self.book_id = book_id
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

    def __repr__(self):
        return (f"Book({self.book_id}, {self.title}, {self.author}, "
                f"{self.description}, {self.rating}, {self.published_date})")


class BookRequest(BaseModel):
    book_id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=3)
    description: str = Field(min_length=1, max_length=100)
    rating: float = Field(ge=0, le=5)
    published_date: int = Field(ge=1700, le=2024)

    class Config:
        json_schema_extra = {
            'example': {
                'title': 'A New Book',
                'author': 'Arpan Moitra',
                'description': 'A description for this book',
                'published_date': 2024,
                'rating': 5
            }
        }


BOOKS = [Book(1, "Computer Science Fundamentals", "Arpan Moitra", "Great Book for CS Fundamentals", 4.9, 2020),
         Book(2, "Learning Fast API", "Arpan Moitra", "Great Book for learning FastAPI", 4.3, 2021),
         Book(3, "Learning Product Management", "Shreyans Jain", "Great book to learn ProdMan", 4.9, 2021),
         Book(4, "Learning Marketing", "Prisha Kumar", "Great book to learn Marketing", 4.7, 2023),
         Book(5, "Learning C++", "Moin Memon", "Great book for learning C++", 4.5, 2022),
         Book(6, "Learning Python", "Samay Varshney", "Great book for learning Python", 4.6, 2022)]


@app.get('/books', status_code=status.HTTP_200_OK)
async def read_all_books():
    return BOOKS


@app.post('/create-book', status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    def _generate_book_id(book: Book):
        book.book_id = 1 if len(BOOKS) == 0 else BOOKS[-1].book_id + 1
        return book

    BOOKS.append(_generate_book_id(Book(**book_request.model_dump())))


@app.get("/books/by-publication-date/", status_code=status.HTTP_200_OK)
async def read_book_by_publication_date(publication_year: int = Query(ge=1700, le=2024)):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == publication_year:
            books_to_return.append(book)

    return books_to_return


@app.get("/books/by-ratings/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: float = Query(ge=0, le=5)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def read_book_by_id(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.book_id == book_id:
            return book

    raise HTTPException(status_code=404, detail="Item not found")


@app.put("/book/update_book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(updated_book: BookRequest):
    is_book_valid = False
    for ind, book in enumerate(BOOKS):
        if book.book_id == updated_book.book_id:
            BOOKS[ind] = Book(**updated_book.model_dump())
            is_book_valid = True

    if not is_book_valid:
        raise HTTPException(status_code=404, detail="Item not found")


@app.delete("/book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    is_book_valid = False
    for ind, book in enumerate(BOOKS):
        if book.book_id == book_id:
            BOOKS.pop(ind)
            is_book_valid = True

    if not is_book_valid:
        raise HTTPException(status_code=404, detail="Item not found")
