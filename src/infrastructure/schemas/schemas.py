from pydantic import BaseModel, Field


class FilmSchema(BaseModel):
    title: str
    director: str
    year: int| None = Field(ge=1800)
    is_deleted: bool = Field(default=False)

