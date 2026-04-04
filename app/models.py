from datetime import datetime
from typing import List, Type

from sqlalchemy import ForeignKey, UniqueConstraint, CheckConstraint, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class ModelBase(DeclarativeBase):
	__abstract__ = True
	id: Mapped[int] = mapped_column('Id',primary_key=True)


class Budget(ModelBase):
	__tablename__ = 'Budgets'

	__table_args__ = (UniqueConstraint('user_id', 'category_id', 'period', name='ux_budgets_user_category_period'),)

	user_id: Mapped[int] = mapped_column('UserId', ForeignKey('Users.Id'))
	category_id: Mapped[int] = mapped_column('CategoryId', ForeignKey('Categories.Id'))
	period: Mapped[str] = mapped_column('Period')
	limit: Mapped[int] = mapped_column('Limit')

	user: Mapped['User'] = relationship(back_populates='budgets')
	category: Mapped['Category'] = relationship(back_populates='budgets')


class Category(ModelBase):
	__tablename__ = 'Categories'
	__table_args__ = (
		UniqueConstraint('user_id', 'name', name='ux_system_category_name'),
		CheckConstraint('(IsSystem = 1 AND UserId IS NULL) OR (IsSystem = 0 AND UserId IS NOT NULL)'),
	)

	name: Mapped[str] = mapped_column('Name')
	user_id: Mapped[int | None] = mapped_column('UserId', ForeignKey('Users.Id'), nullable=True)
	is_system: Mapped[bool] = mapped_column('IsSystem', CheckConstraint('IsSystem IN (0, 1)'), nullable=False, default=False)

	user: Mapped[Type['User'] | None] = relationship(back_populates='categories')
	budgets: Mapped[List['Budget']] = relationship(back_populates='category')
	transactions: Mapped[List['Transaction']] = relationship(back_populates='category')


class Transaction(ModelBase):
	__tablename__ = 'Transactions'

	user_id: Mapped[int] = mapped_column('UserId', ForeignKey('Users.Id'))
	category_id: Mapped[int | None] = mapped_column('CategoryId', ForeignKey('Categories.Id'), nullable=True)
	amount: Mapped[int] = mapped_column('Amount', CheckConstraint('Amount > 0'))
	type: Mapped[str] = mapped_column('Type', CheckConstraint('Type IN ("income", "expense")'))
	description: Mapped[str | None] = mapped_column('Description', nullable=True)
	executed_at: Mapped[datetime] = mapped_column('ExecutedAt')
	created_at: Mapped[datetime] = mapped_column('CreatedAt', server_default=func.current_timestamp())

	user: Mapped['User'] = relationship(back_populates='transactions')
	category: Mapped['Category'] = relationship(back_populates='transactions')


class User(ModelBase):
	__tablename__ = 'Users'

	username: Mapped[str] = mapped_column('Username', unique=True)
	email: Mapped[str] = mapped_column('Email', unique=True)
	password_hash: Mapped[str] = mapped_column('PasswordHash')
	created_at: Mapped[datetime] = mapped_column('CreatedAt', server_default=func.current_timestamp())

	categories: Mapped[List['Category']] = relationship(back_populates='user')
	budgets: Mapped[List['Budget']] = relationship(back_populates='user')
	transactions: Mapped[List['Transaction']] = relationship(back_populates='user')

