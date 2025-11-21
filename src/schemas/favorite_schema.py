# schemas/favorite_schema.py
from pydantic import BaseModel

class FavoriteCreateSchema(BaseModel):
    film_id: int

class FavoriteResponseSchema(BaseModel):
    user_id: int
    film_id: int

    class Config:
        from_attributes = True
