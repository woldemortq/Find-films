from pydantic import BaseModel, Field

class FilmSchema(BaseModel):
    title: str
    director: str | None
    year: int | None
    is_deleted: bool
    type: str

    class Config:
        from_attributes = True


