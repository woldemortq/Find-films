from typing import List
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.db_connect import get_db
from domain.models.FilmModel import FilmModel
from schemas.film_schema import FilmSchema

router = APIRouter(prefix="/films", tags=["Фильмы и сериалы 🎥"])

@router.get(
    "/",
    summary="Получить все фильмы",
)
async def get_films(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(FilmModel))
    films = result.scalars().all()
    if not films:
        raise HTTPException(status_code=404, detail="film list is empty!")
    return films


@router.get(
    "/{film_id}",
    summary="Получить конкретный фильм или сериал по id",
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


@router.post(
    "/",
    summary="Добавить фильм или несколько фильмов",
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


@router.patch("/{film_id}",
           summary="Редактировать фильмы и сериалы",
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


@router.delete("/{film_id}",
           summary="Удалить фильмы и сериалы",
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