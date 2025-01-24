from pydantic import BaseModel,EmailStr


# Pydantic Models
class User(BaseModel):
    id: str
    name: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserCreate(User):
    password: str


class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        orm_mode = True


# Token response model
class Token(BaseModel):
    access_token: str
    token_type: str
