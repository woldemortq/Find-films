from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt

from config.database.db_connect import get_db
from domain.models.UserModel import UserModel
from core.security import decode_access_token
from schemas.login_schema import UserResponseSchema, UserCreateSchema, \
    TokenSchema
from services.auth_services import login_user

router = APIRouter(prefix="/auth", tags=["Регистрация и авторизация 🔐"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register", response_model=UserResponseSchema)
async def register(user: UserCreateSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.username == user.username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode("utf-8")

    new_user = UserModel(
        username=user.username,
        email=user.email,
        password_hash=hashed_password_str
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.username == form_data.username))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.checkpw(form_data.password.encode("utf-8"), existing_user.password_hash.encode("utf-8")):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = await login_user(form_data.username, form_data.password, db)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return payload["user_id"]

@router.get("/protected")
async def protected(user_id: int = Depends(get_current_user)):
    return {"message": "TOP SECRET", "user_id": user_id}
