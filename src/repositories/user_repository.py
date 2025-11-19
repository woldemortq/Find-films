import bcrypt

from domain.models import UserModel


def create_user(username: str, password: str):
    if username in UserModel:
        return {"message": "User already exists"}
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    users[username] = {"password_hash": hashed, "id": len(users) + 1}
    return users[username]

def get_users(username: str):
    return users.get(username)


def validate_password(username: str, password: str):
    user = get_users(username)
    if not user:
        return {"message": "User does not exist"}

    return bcrypt.checkpw(password.encode(), user["password_hash"])