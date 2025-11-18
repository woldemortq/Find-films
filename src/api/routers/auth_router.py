import os

from fastapi import APIRouter, HTTPException, Response, Depends
from authx import AuthX, AuthXConfig

from schemas.login_schema import UserLoginSchema

router = APIRouter(prefix="/auth", tags = ["Регистрация и авторизация 🔐"])

config = AuthXConfig()
config.JWT_SECRET_KEY = os.getenv("SECRET_KEY")
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]

security = AuthX(config=config)



@router.post("/login",
    summary="Авторизация")
async def login(creds: UserLoginSchema, response: Response):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid login")
@router.post("/registration",
    summary="Регистрация",
)
async def registration():
    pass

@router.get("/protected", dependencies=[Depends(security.access_token_required)])
async def protected():
    return {"data": "TOP SECRET"}



