from sqlalchemy import ForeignKey, UniqueConstraint
from ModelBase import ModelBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Budget(ModelBase):
	__tablename__ = 'Budgets'

	__table_args__ = (UniqueConstraint('user_id', 'category_id', 'period', name='ux_budgets_user_category_period'))

	user_id: Mapped[int] = mapped_column(ForeignKey('Users.Id'))
	category_id: Mapped[int] = mapped_column(ForeignKey('Categories.Id'))
	period: Mapped[str] = mapped_column()
	limit: Mapped[int] = mapped_column()

	user: Mapped['User'] = relationship(back_populates='budgets')
	category: Mapped['Category'] = relationship(back_populates='budgets')
