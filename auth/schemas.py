from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    class Config:
        orm_mode = True
