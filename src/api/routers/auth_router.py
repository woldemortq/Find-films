from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags = ["Регистрация и авторизация 🔐"])

@router.post("/",
    summary="Регистрация",
)
async def registration():
    pass