from app import database
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, UniqueConstraint
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship


class User(database.Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default="user")


    is_active = Column(Boolean, default=True)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    events = relationship("Event", back_populates="creator")
    registrations = relationship("Registration", back_populates="user", cascade="all, delete-orphan")


class Event(database.Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    location = Column(String, nullable=False, index=True)
    date = Column(TIMESTAMP(timezone=True), nullable=False)

    capacity = Column(Integer, nullable=True)
    is_published = Column(Boolean, default=False)

    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    creator = relationship("User", back_populates="events")
    registrations = relationship("Registration", back_populates="event", cascade="all, delete-orphan")


class Registration(database.Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False, index=True)

    status = Column(String, nullable=False, default="registered")

    registered_time = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()'))

    __table_args__ = (UniqueConstraint('user_id', 'event_id', name='unique_user_event'),)

    user = relationship("User", back_populates="registrations")
    event = relationship("Event", back_populates="registrations")