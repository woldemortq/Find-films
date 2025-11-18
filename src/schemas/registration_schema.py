from pydantic import BaseModel, EmailStr, field_validator
import re


class RegistrationUserSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

    @field_validator("username")
    def validate_username(cls, value):
        if len(value) < 5:
            raise ValueError("Username must be at least 5 characters long.")
        if len(value) > 20:
            raise ValueError("Username must be no more than 20 characters long.")
        if value.strip() == "":
            raise ValueError("Username cannot be empty.")
        return value

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if not re.search(r"[a-z]", value):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not re.search(r"[A-Z]", value):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not re.search(r"\d", value):
            raise ValueError("Password must contain at least one digit.")

        return value
