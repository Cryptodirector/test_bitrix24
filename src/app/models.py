from src.database.config import Base
from sqlalchemy.orm import Mapped, mapped_column


class Man(Base):
    __tablename__ = 'man'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]


class Woman(Base):
    __tablename__ = 'woman'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]




