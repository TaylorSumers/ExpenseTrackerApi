from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ModelBase import ModelBase


class Transaction(ModelBase):
	__tablename__ = 'Transactions'

	user_id: Mapped[int] = mapped_column(ForeignKey('Users.Id'))
	category_id: Mapped[Optional[int]] = mapped_column(ForeignKey('Categories.Id'), nullable=True)
	amount: Mapped[int] = mapped_column(CheckConstraint('Amount > 0'))
	type: Mapped[str] = mapped_column(CheckConstraint('Type IN ("income", "expense")'))
	description: Mapped[str] = mapped_column(nullable=True)
	executed_at: Mapped[datetime] = mapped_column()
	created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())

	user: Mapped['User'] = relationship(back_populates='transactions')
	category: Mapped['Category'] = relationship(back_populates='transactions')
