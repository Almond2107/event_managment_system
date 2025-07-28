from sqlalchemy import ForeignKey, Integer, String, Text, Enum, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, UTC
from app.database import Base
import enum



class RegistrationStatus(enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    WAITLIST = "waitlist"



class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    username: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    is_verified: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    events = relationship("Event", back_populates="organizer")
    registrations = relationship("EventRegistration", back_populates="user")

class Event(Base):

    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(99), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    start_datetime: Mapped[datetime] = mapped_column(nullable=False)
    end_datetime: Mapped[datetime] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(String(255), nullable=True)
    max_participants: Mapped[int] = mapped_column(nullable=False)
    organizer_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))

    organizer = relationship("User", back_populates="events")
    registrations = relationship("EventRegistration", back_populates="event")

class EventRegistration(Base):

    __tablename__ = "event_registrations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"))
    registred_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))
    status: Mapped[RegistrationStatus] = mapped_column(Enum(RegistrationStatus), default=RegistrationStatus.WAITLIST)

    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")
