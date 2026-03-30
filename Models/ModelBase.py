from abc import ABC
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ModelBase(DeclarativeBase, ABC):
	id: Mapped[int] = mapped_column(primary_key=True)
