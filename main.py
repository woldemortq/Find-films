from typing import List
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.db_connect import get_db
from infrastructure.models.FilmModel import FilmModel
from infrastructure.schemas.schemas import FilmSchema

app = FastAPI()


@app.get(
    "/films",
    summary="Получить все фильмы",
    tags=["Фильмы и сериалы 🎥"],

)
async def get_films(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmModel))
    films = result.scalars().all()
    if not films:
        raise HTTPException(status_code=404, detail="film list is empty!")
    return films


@app.get(
    "/films/{film_id}",
    summary="Получить конкретный фильм или сериал по id",
    tags=["Фильмы и сериалы 🎥"]
)
async def get_one_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmModel).where(FilmModel.id ==
                                                      film_id))
    films = result.scalars().first()
    if not films:
        raise HTTPException(status_code=404,
                            detail=f"Film number {film_id} not "
                                   f"found")
    return films


@app.post(
    "/films",
    summary="Добавить фильм или несколько фильмов",
    tags=["Фильмы и сериалы 🎥"]
)
async def add_film(new_film: List[FilmSchema], db: AsyncSession =
Depends(get_db)):
    added_films = []
    for film in new_film:
        film = FilmModel(
            title=film.title,
            director=film.director,
            year=film.year,
        )
        db.add(film)
        added_films.append(film)

    await db.commit()
    return {"success": True, "message": f"Film, '{film.title}' added "
                                        "successfully"}


@app.patch("/films/{film_id}",
           summary="Редактировать фильмы и сериалы",
           tags=["Фильмы и сериалы 🎥"]
)
async def edit_films(new_film: FilmSchema, film_id: int, db: AsyncSession =
Depends(get_db)):
    result = await db.execute(
        select(FilmModel).where(FilmModel.id == film_id))
    existing_item = result.scalar_one_or_none()

    if existing_item is None:
        return {"error": f"Item {new_film.id} not found"}

    for key, value in new_film.dict(exclude_unset=True).items():
        setattr(existing_item, key, value)


    db.add(existing_item)
    await db.commit()

    return {"message": "Film updated successfully", "film": existing_item}


@app.delete("/films/{film_id}",
           summary="Удалить фильмы и сериалы",
           tags=["Фильмы и сериалы 🎥"]
)
async def delete_films(film_id: int, db: AsyncSession =
Depends(get_db)):
    result_delete = await db.execute(select(FilmModel).where(
        FilmModel.id == film_id, FilmModel.is_deleted == False))
    films_deleted = result_delete.scalar_one_or_none()

    if not films_deleted:
        raise HTTPException(status_code=404, detail=f"Film no. {film_id} not found")

    films_deleted.is_deleted = True
    await db.commit()
    return {"msg": f"Film no. {film_id} deleted successfully"}



if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
