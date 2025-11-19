from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from config.database.db_connect import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    films: Mapped[list["FilmModel"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan")