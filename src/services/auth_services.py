from core.security import create_access_token
from repositories.user_repository import *


def register_user(username: str, password: str):
    user = create_user(username, password)
    return user

def login_user(username: str, password: str):
    if not validate_password(username, password):
        return {"message": "Invalid username or password"}

    user = get_users(username)
    token = create_access_token(user["id"])
    return {"access_token": token, "token_type": "bearer"}