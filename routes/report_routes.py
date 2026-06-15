from fastapi import APIRouter
from database.book_db import BookDB
from database.member_db import MemberDB
from logger_config import logger

router = APIRouter(prefix="/reports", tags=["Reports"])
book_db = BookDB()
member_db = MemberDB()


@router.get("/summary")
def get_library_summary():
    logger.info("Generating general library metrics summary report")
    
    total_books = book_db.count_total_books()
    available_books = book_db.count_available_books()
    currently_borrowed = book_db.count_borrowed_books()
    active_members = member_db.count_active_members()
    
    return {
        "total_books": total_books,
        "available_books": available_books,
        "currently_borrowed": currently_borrowed,
        "active_members": active_members
    }


@router.get("/books-by-genre")
def get_books_by_genre():
    logger.info("Generating books count by genre report")
    
    genres_data = book_db.count_by_genre()
    
    result = []
    for row in genres_data:
        result.append({
            "genre": row[0],
            "count": row[1]
        })
    return result


@router.get("/top-member")
def get_top_member():
    logger.info("Generating top member report")
    
    top_member_data = member_db.get_top_member()
    
    if not top_member_data:
        logger.info("Top member query executed, but no members exist yet")
        return {"member_id": None, "borrows_total": 0}
        
    return {
        "member_id": top_member_data[0],
        "borrows_total": top_member_data[1]
    }