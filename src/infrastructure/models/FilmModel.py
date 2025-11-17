from sqlalchemy.orm import Mapped, mapped_column
from src.config.database.db_connect import Base


class FilmModel(Base):
    __tablename__ = "films"

    id:Mapped[int] = mapped_column(primary_key=True)
    title:Mapped[str] = mapped_column(nullable=False)
    director:Mapped[str] = mapped_column(nullable=False)
    year:Mapped[int] = mapped_column(nullable=False)
    deleted:Mapped[bool] = mapped_column(nullable=False, default=False)