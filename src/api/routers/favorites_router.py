from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config.database.db_connect import get_db
from domain.models import FavoriteModel, FilmModel, UserModel
from schemas.favorite_schema import FavoriteCreateSchema, FavoriteResponseSchema
from api.routers.auth_router import get_current_user

router = APIRouter(prefix="/favorites", tags=["Избранное ⭐"])

@router.post("/", response_model=FavoriteResponseSchema)
async def add_to_favorites(
    favorite: FavoriteCreateSchema,
    user_id: int = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(FilmModel).where(FilmModel.id == favorite.film_id))
    film = result.scalars().first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")

    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    result = await db.execute(
        select(FavoriteModel)
        .where(FavoriteModel.user_id == user_id)
        .where(FavoriteModel.film_id == favorite.film_id)
    )
    existing_favorite = result.scalars().first()
    if existing_favorite:
        raise HTTPException(status_code=400, detail="Film already in favorites")

    new_favorite = FavoriteModel(user_id=user_id, film_id=favorite.film_id)
    db.add(new_favorite)
    await db.commit()
    await db.refresh(new_favorite)

    return new_favorite
