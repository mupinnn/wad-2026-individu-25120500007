from typing import Annotated, Literal
from fastapi import FastAPI, Query, Path, Request, Response, status
from pydantic import BaseModel, Field, StringConstraints, ConfigDict

app = FastAPI()

books = [
    {
        "id": 1,
        "isbn": "1234567817876",
        "judul": "Harry Potter dan Batu Bertuah",
        "tahun_terbit": 2001,
        "pengarang": "J.K. Rowling",
        "penerbit": "Gramedia",
        "jumlah_halaman": 300
    },
    {
        "id": 2,
        "isbn": "1234567817877",
        "judul": "Hungry Games - The First Book",
        "tahun_terbit": 2002,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 374
    },
    {
        "id": 3,
        "isbn": "1234567817878",
        "judul": "The Hunger Games",
        "tahun_terbit": 2008,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    },
    {
        "id": 4,
        "isbn": "1234567817879",
        "judul": "The Hunger Games - The Second Book",
        "tahun_terbit": 2009,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 392
    },
    {
        "id": 5,
        "isbn": "1234567817880",
        "judul": "The Hunger Games - The Third Book",
        "tahun_terbit": 2010,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    },
    {
        "id": 6,
        "isbn": "1234567817881",
        "judul": "The Hunger Games - The Fourth Book",
        "tahun_terbit": 2011,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    },
    {
        "id": 7,
        "isbn": "1234567817882",
        "judul": "The Hunger Games - The Fifth Book",
        "tahun_terbit": 2012,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    },
    {
        "id": 8,
        "isbn": "1234567817883",
        "judul": "The Hunger Games - The Sixth Book",
        "tahun_terbit": 2013,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    },
    {
        "id": 9,
        "isbn": "1234567817884",
        "judul": "The Hunger Games - The Seventh Book",
        "tahun_terbit": 2014,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    },
    {
        "id": 10,
        "isbn": "1234567817885",
        "judul": "The Hunger Games - The Eighth Book",
        "tahun_terbit": 2015,
        "pengarang": "Suzanne Collins",
        "penerbit": "Scholastic",
        "jumlah_halaman": 420
    }
]

@app.get("/health")
def get_health():
    return {"status": "ok"}

class GetBooksFilterParams(BaseModel):
    limit: int | None = Field(5, ge=5, le=100)
    skip: int | None = Field(0, ge=0)
    search: Annotated[str, StringConstraints(to_lower=True)] | None = None

@app.get("/books")
def get_books(q: Annotated[GetBooksFilterParams, Query()]):
    results = books

    if q.search:
        results = [book for book in books if q.search in book['judul'].lower()]

    return results[q.skip : q.skip + q.limit]

@app.get("/books/{id}")
def get_books_by_id(id: Annotated[int, Path(title="ID dari buku yang ingin dilihat detailnya")], response: Response):
    res = [book for book in books if id == book['id']]
    res = res[0] if res else None

    if res == None:
        response.status_code = status.HTTP_404_NOT_FOUND
        res = {"status": "not found", "message": "Buku yang kamu cari tidak ditemukan."}

    return res

class BookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    isbn: str
    judul: str
    tahun_terbit: int
    pengarang: str
    penerbit: str
    jumlah_halaman: int

class Book(BookCreate):
    id: int

@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
def create_books(book: BookCreate, request: Request, response: Response):
    new_id = max((b["id"] for b in books), default=0) + 1
    new_book = {"id": new_id, **book.model_dump()}
    books.append(new_book)

    response.headers["Location"] = str(request.url_for("get_books_by_id", id=new_id))
    return new_book
