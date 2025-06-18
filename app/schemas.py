from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ElectionCreate(BaseModel):
    title: str
    description: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: datetime

class ElectionOut(BaseModel):
    id: int
    title: str
    description: Optional[str]
    start_time: datetime
    end_time: datetime
    is_active: bool

    class Config:
        orm_mode = True

class TokenBatchRequest(BaseModel):
    election_id: int
    count: int

class VoterTokenOut(BaseModel):
    token: str

    class Config:
        orm_mode = True
