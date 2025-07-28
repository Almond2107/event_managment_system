from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.models.models import Event, EventRegistration, User
from app.schemas.schemas import EventCreate, EventResponse
from app.utils.dependencies import db_dep, get_current_user

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=List[EventResponse])
async def list_all_events(db: db_dep):
    events = db.query(Event).filter(Event.is_active == True).all()
    return events


@router.post("/", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate, db: db_dep, user: User = Depends(get_current_user)):
    new_event = Event(**event.dict(), organizer_id=user.id)
    db.add(new_event)
    db.commit()
    db.refresh(new_event)
    return new_event


@router.get("/{id}", response_model=EventResponse)
async def get_event(id: int, db: db_dep):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    return event



@router.put("/{id}", response_model=EventResponse)
async def update_event(id: int, updated: EventCreate, db: db_dep, user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    if event.organizer_id != user.id:
        raise HTTPException(403, "You are not the organizer of this event")

    for key, value in updated.dict().items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event



@router.delete("/{id}", status_code=204)
async def delete_event(id: int, db: db_dep, user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(404, "Event not found")
    if event.organizer_id != user.id:
        raise HTTPException(403, "You are not organizer")

    db.delete(event)
    db.commit()
    return



@router.post("/{id}/register", status_code=201)
async def register_event(id: int, db: db_dep, user: User = Depends(get_current_user)):
    event = db.query(Event).filter(Event.id == id).first()
    if not event:
        raise HTTPException(404, "Event not found")

    existing = db.query(EventRegistration).filter_by(user_id=user.id, event_id=id).first()
    if existing:
        raise HTTPException(400, "Already registered")

    count = db.query(EventRegistration).filter_by(event_id=id).count()
    if count >= event.max_participants:
        raise HTTPException(400, "Participant limit reached")

    register_eve = EventRegistration(user_id=user.id, event_id=id)
    db.add(register_eve)
    db.commit()
    return {"msg": "Registered"}



@router.delete("/{id}/register", status_code=204)
async def cancel_registration(id: int, db: db_dep, user: User = Depends(get_current_user)):
    register_del = db.query(EventRegistration).filter_by(user_id=user.id, event_id=id).first()
    if not register_del:
        raise HTTPException(404, "Registration not found")

    db.delete(register_del)
    db.commit()
    return




@router.get("/{id}/participants")
async def list_participants(id: int, db: db_dep, user: User = Depends(get_current_user)):
    event_participants = db.query(Event).filter(Event.id == id).first()
    if not event_participants:
        raise HTTPException(404, "Event not found")
    if event_participants.organizer_id != user.id:
        raise HTTPException(403, "You are not the organizer")

    regs = db.query(EventRegistration).filter_by(event_id=id).all()
    return [{"user_id": reg.user_id, "status": reg.status.name} for reg in regs]


