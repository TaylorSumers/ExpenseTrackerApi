from abc import ABC
from datetime import datetime
from typing import Optional, List

from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class ModelBase(DeclarativeBase, ABC):
	id: Mapped[int] = mapped_column(primary_key=True)


class Budget(ModelBase):
	__tablename__ = 'Budgets'

	__table_args__ = (UniqueConstraint('user_id', 'category_id', 'period', name='ux_budgets_user_category_period'))

	user_id: Mapped[int] = mapped_column(ForeignKey('Users.Id'))
	category_id: Mapped[int] = mapped_column(ForeignKey('Categories.Id'))
	period: Mapped[str] = mapped_column()
	limit: Mapped[int] = mapped_column()

	user: Mapped['User'] = relationship(back_populates='budgets')
	category: Mapped['Category'] = relationship(back_populates='budgets')


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


class User(ModelBase):
	__tablename__ = 'Users'

	username: Mapped[str] = mapped_column(unique=True)
	email: Mapped[str] = mapped_column(unique=True)
	password_hash: Mapped[str] = mapped_column()
	created_at: Mapped[datetime] = mapped_column(server_default=func.current_timestamp())

	categories: Mapped[List['Category']] = relationship(back_populates='user')
	budgets: Mapped[List['Budget']] = relationship(back_populates='user')
	transactions: Mapped[List['Transaction']] = relationship(back_populates='user')
