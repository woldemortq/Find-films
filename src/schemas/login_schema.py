from pydantic import BaseModel


class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserCreateSchema(BaseModel):
    username: str
    email: str
    password: str

class UserResponseSchema(BaseModel):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True

class TokenSchema(BaseModel):
    access_token: str
    token_type: str
