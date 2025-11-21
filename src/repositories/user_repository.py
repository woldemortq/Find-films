from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from config.database.db_connect import get_db
from domain.models import UserModel

async def create_user(username: str, password: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    if user:
        return {"message": "User already exists"}

    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf-8')

    new_user = UserModel(username=username, password_hash=hashed)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user(username: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.username == username))
    user = result.scalars().first()
    return user

async def validate_password(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await get_user(username, db)
    if not user:
        return {"message": "User does not exist"}

    if bcrypt.checkpw(password.encode(), user.password_hash.encode('utf-8')):
        return {"message": "Password is correct"}
    else:
        return {"message": "Incorrect password"}
