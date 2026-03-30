from typing import Optional, List
from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ModelBase import ModelBase


class Сategory(ModelBase):
	__tablename__ = 'Categories'
	__table_args__ = (
		UniqueConstraint('user_id', 'name', name='ux_system_category_name'),
		CheckConstraint('IsSystem = 1 AND UserId IS NULL) OR (IsSystem = 0 AND UserId IS NOT NULL)'),
	)

	name: Mapped[str] = mapped_column()
	user_id: Mapped[Optional[int]] = mapped_column(ForeignKey('Users.Id'), nullable=True)
	is_system: Mapped[bool] = mapped_column(CheckConstraint('IsSystem IN (0, 1)'), nullable=False, default=False)

	user: Mapped[Optional['User']] = relationship(back_populates='categories')
	budgets: Mapped[List['Budget']] = relationship(back_populates='category')
	transactions: Mapped[List['Transaction']] = relationship(back_populates='category')
