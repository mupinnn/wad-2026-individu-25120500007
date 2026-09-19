from typing import Annotated, Literal
from pydantic import BaseModel, Field, StringConstraints, ConfigDict

class GetBooksFilterParams(BaseModel):
    limit: int | None = Field(5, ge=5, le=100)
    skip: int | None = Field(0, ge=0)
    search: Annotated[str, StringConstraints(to_lower=True)] | None = None

class BookCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    isbn: str = Field(min_length=13, max_length=13, pattern=r"^\d{13}$")
    judul: str
    tahun_terbit: int = Field(ge=1900, le=2026)
    pengarang: str
    penerbit: str
    jumlah_halaman: int

class Book(BookCreate):
    id: int

