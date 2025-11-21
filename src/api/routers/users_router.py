from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.database.db_connect import get_db
from domain.models.UserModel import UserModel
from schemas.user_schema import UserSchema

router = APIRouter(prefix="/users", tags=["Пользователи 🙍🏻‍♂️"])

@router.get("/", summary="Получить список всех пользователей", response_model=list[UserSchema])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel))
    users = result.scalars().all()
    if not users:
        raise HTTPException(status_code=404, detail="Users list is empty!")
    return users

@router.get("/{user_id}", summary="Получить пользователя по id", response_model=UserSchema)
async def get_one_user(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found!")
    return user
