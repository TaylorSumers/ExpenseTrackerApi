from datetime import datetime
from typing import List

from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.testing.schema import mapped_column
import Category, Budget

from Models.ModelBase import ModelBase


class User(ModelBase):
	__tablename__ = 'Users'

	username: Mapped[str] = mapped_column(unique=True)
	email: Mapped[str] = mapped_column(unique=True)
	password_hash: Mapped[int] = mapped_column()
	created_at: Mapped[datetime] = mapped_column()

	categories: Mapped[List[Category]] = relationship(back_populates='user')
	budgets: Mapped[List[Budget]] = relationship(back_populates='user')
