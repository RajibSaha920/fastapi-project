from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from database import get_db
import model

app = FastAPI()

# Input schema
class BookStore(BaseModel):
    title: str
    author: str
    publish_date: str  # must match SQLAlchemy column

    class Config:
        orm_mode = True

# Response schema
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

    class Config:
        orm_mode = True

# POST: create a new book
@app.post("/books", response_model=BookResponse)
def create_book(book: BookStore, db: Session = Depends(get_db)):
    new_book = model.Book(
        title=book.title,
        author=book.author,
        publish_date=book.publish_date
    )
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

# GET: fetch all books
@app.get("/books", response_model=list[BookResponse])
def get_books(db: Session = Depends(get_db)):
    return db.query(model.Book).all()