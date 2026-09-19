from typing import Annotated
from fastapi import FastAPI, HTTPException, Query, Path, Request, Response, status

from app.schemas import Book, BookCreate, GetBooksFilterParams
from app.services import create_book, get_book, list_books

app = FastAPI()

@app.get("/health")
def get_health():
    return {"status": "ok"}

@app.get("/books", response_model=list[Book])
def get_books(q: Annotated[GetBooksFilterParams, Query()]):
    return list_books(q)

@app.get("/books/{id}", response_model=Book)
def get_books_by_id(id: Annotated[int, Path(title="ID dari buku yang ingin dilihat detailnya")], response: Response):
    book = get_book(id)

    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "not found", "message": "Buku yang kamu cari tidak ditemukan."}
        )

    return book

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_books(book: BookCreate, request: Request, response: Response):
    new_book = create_book(book)
    response.headers["Location"] = str(request.url_for("get_books_by_id", id=new_book["id"]))

    return new_book
