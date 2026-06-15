from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from database.member_db import MemberDB
from mysql.connector import IntegrityError
from logger_config import logger

router = APIRouter(prefix="/members", tags=["Members"])
member_db = MemberDB()

class MemberCreateSchema(BaseModel):
    name: str = Field(..., max_length=50)
    email: EmailStr  

class MemberUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=50)
    email: Optional[EmailStr] = None


@router.post("", status_code=status.HTTP_201_CREATED)
def create_member(member: MemberCreateSchema):
    logger.info(f"Attempting to register new member: name='{member.name}', email='{member.email}'")
    try:
        member_db.create_member(member.name, member.email)
        logger.info(f"Member '{member.name}' registered successfully")
        return {"message": "Member created successfully"}
    except IntegrityError as e:
        logger.warning(f"Registration failed: Email '{member.email}' already exists. Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )


@router.get("")
def get_all_members():
    logger.info("Fetching all members from database")
    members = member_db.get_all_members()
    
    result = []
    for m in members:
        result.append({
            "id": m[0],
            "name": m[1],
            "email": m[2],
            "is_active": bool(m[3]),
            "borrows_total": m[4]
        })
    return result


@router.get("/{id}")
def get_member_by_id(id: int):
    logger.info(f"Fetching member with ID: {id}")
    member = member_db.get_member_by_id(id)
    if not member:
        logger.warning(f"Member with ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    return {
        "id": member[0],
        "name": member[1],
        "email": member[2],
        "is_active": bool(member[3]),
        "borrows_total": member[4]
    }


@router.patch("/{id}")
def update_member(id: int, member_data: MemberUpdateSchema):
    logger.info(f"Attempting to update member ID {id}")
    
    current_member = member_db.get_member_by_id(id)
    if not current_member:
        logger.warning(f"Update failed: Member ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    name = member_data.name if member_data.name is not None else current_member[1]
    email = member_data.email if member_data.email is not None else current_member[2]
    
    try:
        member_db.update_member(name, email, id)
        logger.info(f"Member ID {id} updated successfully")
        return {"message": "Member updated successfully"}
    except IntegrityError as e:
        logger.warning(f"Update failed: Email '{email}' is already taken by another member. Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )


@router.patch("/{id}/deactivate")
def deactivate_member(id: int):
    logger.info(f"Attempting to deactivate member ID {id}")
    
    member = member_db.get_member_by_id(id)
    if not member:
        logger.warning(f"Deactivation failed: Member ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    member_db.deactivate_member(id)
    logger.info(f"Member ID {id} has been deactivated successfully")
    return {"message": "Member deactivated successfully"}


@router.patch("/{id}/activate")
def activate_member(id: int):
    logger.info(f"Attempting to activate member ID {id}")
    
    member = member_db.get_member_by_id(id)
    if not member:
        logger.warning(f"Activation failed: Member ID {id} not found")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
        
    member_db.activate_member(id)
    logger.info(f"Member ID {id} has been activated successfully")
    return {"message": "Member activated successfully"}