from datetime import datetime
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Mapped, relationship, mapped_column

from models.model_base import ModelBase


class User(ModelBase):
	__tablename__ = 'Users'

	username: Mapped[str] = mapped_column(unique=True)
	email: Mapped[str] = mapped_column(unique=True)
	password_hash: Mapped[str] = mapped_column()
	created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())

	categories: Mapped[List['Category']] = relationship(back_populates='user')
	budgets: Mapped[List['Budget']] = relationship(back_populates='user')
	transactions: Mapped[List['Transaction']] = relationship(back_populates='user')
