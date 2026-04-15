from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app import models, schemas, deps

router = APIRouter(
    prefix="/events",
    tags=["events"],
    # dependencies=[Depends(Oauth2.required_role("admin"))],
) 

@router.post("/", response_model=schemas.Event)
def create_event(event_create: schemas.EventCreate, db: Session = Depends(get_db), 
    current_user: models.User = Depends(deps.get_current_active_user), require_roles=deps.require_roles("admin", "organizer")):
    event = models.Event(
        title=event_create.title,
        description=event_create.description,
        location=event_create.location,
        date=event_create.date,
        capacity=event_create.capacity,
        is_published=event_create.is_published,
        creator_id=current_user.id
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    
    return event

@router.get("/{event_id}", response_model=schemas.Event)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")
    return event

@router.put("/{event_id}", response_model=schemas.Event)
def update_event(event_id: int, event_update: schemas.EventCreate, db: Session = Depends(get_db), 
    current_user: models.User = Depends(deps.get_current_active_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # Check if the current user is the creator of the event
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this event")

    for key, value in event_update.dict(exclude_unset=True).items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event

@router.delete("/{event_id}")
def delete_event(event_id: int, db: Session = Depends(get_db), 
    current_user: models.User = Depends(deps.get_current_active_user)):
    event = db.query(models.Event).filter(models.Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Event not found")

    # Check if the current user is the creator of the event
    if event.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this event")

    db.delete(event)
    db.commit()
    return {"detail": "Event deleted successfully"}

@router.get("/", response_model=List[schemas.Event])
def list_events(db: Session = Depends(get_db)):
    events = db.query(models.Event).all()
    return events


@router.get("/events/{event_id}/registrations", response_model=List[schemas.Registration])
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
