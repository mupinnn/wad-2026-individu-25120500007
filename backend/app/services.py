from app.schemas import BookCreate, GetBooksFilterParams

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

def list_books(q: GetBooksFilterParams) -> list[dict]:
    results = books

    if q.search:
        results = [book for book in books if q.search in book['judul'].lower()]

    return results[q.skip : q.skip + q.limit]

def get_book(book_id: int) -> dict | None:
    for book in books:
        if book["id"] == book_id:
            return book

    return None

def create_book(payload: BookCreate) -> dict:
    new_id = max((b["id"] for b in books), default=0) + 1
    new_book = {"id": new_id, **payload.model_dump()}
    books.append(new_book)
    return new_book

