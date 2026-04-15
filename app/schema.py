from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from datetime import datetime



class UserBase(BaseModel):
    name: str
    email: str
    is_active: Optional[bool] = True
    role: Optional[str] = "user"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"



class User(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventResponse(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date: datetime
    capacity: Optional[int] = None
    is_published: Optional[bool] = False


class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    location: str
    date: datetime
    capacity: Optional[int] = None
    is_published: Optional[bool] = False

    @field_validator("date", mode="before")
    def parse_date(cls, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                try:
                    return datetime.strptime(value, "%B %d, %Y")
                except ValueError:
                    raise ValueError("date must be a valid ISO datetime string or a 'Month day, year' string")
        return value


class Event(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    location: str
    date: datetime
    capacity: Optional[int] = None
    is_published: bool = False
    creator_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True



class RegistrationBase(BaseModel):
    user_id: int
    event_id: int


class RegistrationCreate(RegistrationBase):
    pass


class Registration(RegistrationBase):
    id: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: Optional[int] = None