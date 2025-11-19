import bcrypt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from config.database.db_connect import get_db
from domain.models import UserModel
from services.auth_services import register_user, login_user
from core.security import decode_access_token

router = APIRouter(prefix="/auth", tags = ["Регистрация и авторизация 🔐"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

@router.post("/register")
async def register(username: str, password: str, db: AsyncSession =
Depends(get_db)):
    result = await db.execute(select(UserModel).where(UserModel.username == username))
    existing_user = result.scalars().first()
    if existing_user:
        raise HTTPException(status_code=404, detail="User already exists")
    hashed_password = bcrypt.hash(password)

    new_user = UserModel(username=username, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "User registered successfully", "user_id":
        new_user.id}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(),
                db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(UserModel).where(UserModel.username
                                                      ==
                                                      form_data.username))
    existing_user = result.scalars().first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not "
                                                    "found")
    if not bcrypt.verify(form_data.password, existing_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    token = login_user(form_data.username, form_data.password, )
    if not token:
        raise HTTPException(401, "Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    return payload["user_id"]


@router.get("/protected")
async def protected(user_id: int = Depends(get_current_user)):
    return {"message": "TOP SECRET", "user_id": user_id}
