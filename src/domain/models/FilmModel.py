from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, ForeignKey
from config.database.db_connect import Base


class FilmModel(Base):
    __tablename__ = "films"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    director: Mapped[str] = mapped_column(String, nullable=True)
    year: Mapped[int] = mapped_column(Integer, nullable=True)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    type: Mapped[str] = mapped_column(String, nullable=False,
                                      default='Фильм')


    favorites: Mapped[list["FavoriteModel"]] = relationship(
        "FavoriteModel", back_populates="film",
        cascade="all, delete-orphan"
    )
