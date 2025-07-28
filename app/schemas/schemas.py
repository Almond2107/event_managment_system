from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str = Field(min_length=6, max_length=16)


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    username: str
    is_active: bool
    is_verified: bool
    created_at: datetime


############EVENT##############

class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str] = None
    max_participants: int


class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_datetime: datetime
    end_datetime: datetime
    location: Optional[str]
    max_participants: int
    is_active: bool
    created_at: datetime
    organizer_id: int



#############Registration#############

class RegistrationStatus(str, Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLIST = "waitlist"


class RegistrationCreate(BaseModel):
    event_id: int
    status: RegistrationStatus = RegistrationStatus.WAITLIST


class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    registered_at: datetime
    status: RegistrationStatus



##########Login/Register###########

class UserLogin(BaseModel):
    email: EmailStr
    password: str 





##########TokenRespose##############
class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


