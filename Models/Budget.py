from sqlalchemy import ForeignKey
import User, Category, ModelBase
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Budget(ModelBase):
	__tablename__ = 'Budgets'

	user_id: Mapped[int] = mapped_column(ForeignKey('Users.Id'))
	category_id: Mapped[int] = mapped_column(ForeignKey('Categories.Id'))
	Period: Mapped[str] = mapped_column()
	Limit: Mapped[int] = mapped_column()

	user: Mapped[User] = relationship(back_populates='budgets')
	category: Mapped[Category] = relationship(back_populates='budgets')
