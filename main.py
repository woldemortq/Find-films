import uvicorn
from fastapi import FastAPI

from api.routers.films_router import router as films_router
from api.routers.auth_router import router as auth_router

app = FastAPI(title="Serials and Films API")

app.include_router(films_router)
app.include_router(auth_router)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
