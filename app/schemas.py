# app/schemas.py

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List


class ElectionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None  # Hazlo opcional si permites null


class ElectionOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    is_active: bool

    model_config = {
        "from_attributes": True
    }


class TokenBatchRequest(BaseModel):
    election_id: int
    count: int


class VoterTokenOut(BaseModel):
    token: str

    model_config = {
        "from_attributes": True
    }


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_superuser: bool
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None
