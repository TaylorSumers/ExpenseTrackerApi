from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from Models.ModelBase import ModelBase


class Transaction(ModelBase):
	__tablename__ = 'Transactions'

	user_id: Mapped[int] = mapped_column(ForeignKey('Users.Id'))
	category_id: Mapped[int] = mapped_column(ForeignKey('Categories.Id'), nullable=True)
	amount: Mapped[int] = mapped_column()
	type: Mapped[str] = mapped_column()
	description: Mapped[str] = mapped_column(nullable=True)
	executed_at: Mapped[datetime] = mapped_column()
	created_at: Mapped[datetime] = mapped_column()
