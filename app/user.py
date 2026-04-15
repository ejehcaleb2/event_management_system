from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, utils, deps

router = APIRouter(
    prefix="/users",
    tags=["users"],
)

@router.get("/users/me", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), 
    current_user: models.User = Depends(deps.get_current_active_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if user.id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this user")
    
    db.delete(user)
    db.commit()

@router.get("/users/{user_id}", response_model=schemas.User)
def switch_user_role(user_id: int, new_role: str, db: Session = Depends(get_db), 
    current_user: models.User = Depends(deps.get_current_active_user)):
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to change user roles")
    
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if new_role not in ["admin", "organizer", "attendee"]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid role")
    
    user.role = new_role
    db.commit()
    db.refresh(user)
    
    return user