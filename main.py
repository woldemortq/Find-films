import uvicorn
from fastapi import FastAPI

from api.routers.favorites_router import router as favorites_router
from api.routers.films_router import router as films_router
from api.routers.auth_router import router as auth_router
from api.routers.users_router import router as users_router

app = FastAPI(title="Поиск фильмов и сериалов")

app.include_router(films_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(favorites_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
