from typing import Optional
import User
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class category(DeclarativeBase):
	__tablename__ = 'Categories'

	name: Mapped[str] = mapped_column()
	user_id: Mapped[int] = mapped_column(ForeignKey('Users.Id'), nullable=True)
	is_system: Mapped[bool] = mapped_column()

	user: Mapped[Optional[User]] = relationship(back_populates='categories')