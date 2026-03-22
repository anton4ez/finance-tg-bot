from sqlalchemy import String, Float, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, declarative_base
from datetime import datetime


Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[str | None] = mapped_column(String(50), unique=True)
    first_name: Mapped[str | None] = mapped_column(String(50), nullable=True)
    last_name: Mapped[str | None] = mapped_column(nullable=True)
    register_date: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="user")

    def __repr__(self):
        return f'Пользователь №{self.id}: {self.last_name} {self.first_name}, айди {self.telegram_id}'


class Transaction(Base):
    __tablename__ = 'transactions'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    amount: Mapped[int] = mapped_column(nullable=False)
    category: Mapped[str] = mapped_column(nullable=False)
    transaction_date: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)

    user: Mapped["User"] = relationship(back_populates="transactions")

    def __repr__(self):
        return f'Транзакция №{self.id} от пользователя №{self.user_id}: сумма {self.amount} в категории {self.category}'
