from fastapi import APIRouter, HTTPException
from authx import AuthX, AuthXConfig
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags = ["Регистрация и авторизация 🔐"])

config = AuthXConfig()
config.JWT_SECRET_KEY = "12i3hjowd2uun9u2fiewfn2p3npijnefiwnef"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]


security = AuthX(config=config)

class UserLoginSchema(BaseModel):
    username: str
    password: str

@router.post("/login",
    summary="Авторизация")
async def login(creds: UserLoginSchema):
    if creds.username == "test" and creds.password == "test":
        token = security.create_access_token(uid="12345")
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Invalid login")
@router.post("/registration",
    summary="Регистрация",
)
async def registration():
    pass



