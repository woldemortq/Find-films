from __future__ import annotations
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, TIMESTAMP, func
from config.database.db_connect import Base


class FavoriteModel(Base):
    __tablename__ = "favorites"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    film_id: Mapped[int] = mapped_column(ForeignKey("films.id"), primary_key=True)
    added_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, server_default=func.now(), nullable=False)

    user: Mapped["UserModel"] = relationship("UserModel", back_populates="favorites")
    film: Mapped["FilmModel"] = relationship("FilmModel", back_populates="favorites")
