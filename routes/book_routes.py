from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import Optional
from database.book_db import BookDB
from database.member_db import MemberDB
from logger_config import logger

router = APIRouter(prefix="/books", tags=["Books"])
book_db = BookDB()
member_db = MemberDB()

ALLOWED_GENRES = {"Fiction", "Non-Fiction", "Science", "History", "Other"}

class BookCreateSchema(BaseModel):
    title: str = Field(..., max_length=50)
    author: str = Field(..., max_length=50)
    genre: str

class BookUpdateSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=50)
    author: Optional[str] = Field(None, max_length=50)
    genre: Optional[str] = None


@router.post("", status_code=status.HTTP_201_CREATED)
def create_book(book: BookCreateSchema):
    logger.info(f"Attempting to create book: title='{book.title}', author='{book.author}'")
    
    if book.genre not in ALLOWED_GENRES:
        logger.warning(f"Validation failed: Invalid genre '{book.genre}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid genre. Allowed genres are: {', '.join(ALLOWED_GENRES)}"
        )
        
    book_db.create_book(book.title, book.author, book.genre)
    logger.info(f"Book '{book.title}' created successfully")
    return {"message": "Book created successfully"}


@router.get("")
def get_all_books():
    logger.info("Fetching all books from database")
    books = book_db.get_all_books()
    
    result = []
    for b in books:
        result.append({
            "id": b[0],
            "title": b[1],
            "author": b[2],
            "genre": b[3],
            "is_available": bool(b[4]),
            "borrowed_by_member_id": b[5]
        })
    return result


@router.get("/{id}")
def get_book_by_id(id: int):
    logger.info(f"Fetching book with ID: {id}")
    book = book_db.get_book_by_id(id)
    if not book:
        logger.warning(f"Book with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
    return {
        "id": book[0],
        "title": book[1],
        "author": book[2],
        "genre": book[3],
        "is_available": bool(book[4]),
        "borrowed_by_member_id": book[5]
    }


@router.patch("/{id}")
def update_book(id: int, book_data: BookUpdateSchema):
    logger.info(f"Attempting to update book ID {id}")
    
    current_book = book_db.get_book_by_id(id)
    if not current_book:
        logger.warning(f"Update failed: Book ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
    if book_data.genre is not None and book_data.genre not in ALLOWED_GENRES:
        logger.warning(f"Update failed: Invalid genre '{book_data.genre}'")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid genre. Allowed genres are: {', '.join(ALLOWED_GENRES)}"
        )
        
    title = book_data.title if book_data.title is not None else current_book[1]
    author = book_data.author if book_data.author is not None else current_book[2]
    genre = book_data.genre if book_data.genre is not None else current_book[3]
    
    book_db.update_book(title, author, genre, id)
    logger.info(f"Book ID {id} updated successfully")
    return {"message": "Book updated successfully"}


@router.patch("/{id}/borrow/{member_id}")
def borrow_book(id: int, member_id: int):
    logger.info(f"Process started: Member ID {member_id} attempting to borrow Book ID {id}")
    
    book = book_db.get_book_by_id(id)
    if not book:
        logger.warning(f"Borrow failed: Book ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
    member = member_db.get_member_by_id(member_id)
    if not member:
        logger.warning(f"Borrow failed: Member ID {member_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    is_available = bool(book[4])
    if not is_available:
        logger.warning(f"Borrow failed: Book ID {id} is already borrowed")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book is not available")
        
    is_active = bool(member[3])
    if not is_active:
        logger.warning(f"Borrow failed: Member ID {member_id} is inactive")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member is not active")
        
    current_borrows = book_db.count_active_borrows_by_member(member_id)
    if current_borrows >= 3:
        logger.warning(f"Borrow failed: Member ID {member_id} has reached maximum borrows limit")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Member has reached maximum borrows")
        
    book_db.set_available(id, False, member_id)      
    member_db.increment_borrows(member_id)            
    
    logger.info(f"Success: Book ID {id} borrowed by Member ID {member_id}")
    return {"message": "Book borrowed successfully"}


@router.patch("/{id}/return/{member_id}")
def return_book(id: int, member_id: int):
    logger.info(f"Process started: Member ID {member_id} attempting to return Book ID {id}")
    
    book = book_db.get_book_by_id(id)
    if not book:
        logger.warning(f"Return failed: Book ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")
        
    member = member_db.get_member_by_id(member_id)
    if not member:
        logger.warning(f"Return failed: Member ID {member_id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    borrowed_by = book[5]
    if borrowed_by is None or borrowed_by != member_id:
        logger.warning(f"Return failed: Book ID {id} is not borrowed by Member ID {member_id}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book was not borrowed by this member")
        
    book_db.set_available(id, True, None)
    
    logger.info(f"Success: Book ID {id} returned successfully by Member ID {member_id}")
    return {"message": "Book returned successfully"}