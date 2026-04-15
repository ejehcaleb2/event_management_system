from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, Oauth2, deps

router = APIRouter(
    prefix="/registrations",
    tags=["registration"],
)

@router.post("/{event_id}/register", response_model=schemas.Registration)
def register_for_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    existing_registration = db.query(models.Registration).filter(
        models.Registration.user_id == current_user.id,
        models.Registration.event_id == event_id
    ).first()
    
    if existing_registration:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Already registered for this event")
    
    registration = models.Registration(user_id=current_user.id, event_id=event_id)
    db.add(registration)
    db.commit()
    db.refresh(registration)
    
    return registration

@router.get("/my-registrations", response_model=List[schemas.Registration])
def get_my_registrations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    registrations = db.query(models.Registration).filter(models.Registration.user_id == current_user.id).all()
    return registrations

@router.delete("/{registration_id}/cancel")
def cancel_registration(
    registration_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    registration = db.query(models.Registration).filter(models.Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    
    if registration.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to cancel this registration")
    
    
    db.delete(registration)
    db.commit()
    
    return {"detail": "Registration cancelled successfully"}


@router.get("/event/{event_id}/registrations", response_model=List[schemas.Registration])
def get_event_registrations(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view registrations for this event")
    
    registrations = db.query(models.Registration).filter(models.Registration.event_id == event_id).all()
    return registrations


@router.get("/users/me/registrations", response_model=List[schemas.Registration])
def get_my_registrations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    registrations = db.query(models.Registration).filter(models.Registration.user_id == current_user.id).all()
    return registrations

@router.get("/registration{id}")
def get_registration(registration_id: int, db: Session = Depends(get_db), 
    current_user: models.User = Depends(deps.get_current_active_user)):
    registration = db.query(models.Registration).filter(models.Registration.id == registration_id).first()
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    
    if registration.user_id != current_user.id and registration.event.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to view this registration")