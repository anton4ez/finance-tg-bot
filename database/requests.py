from sqlalchemy import select, func
from sqlalchemy.orm import Session
from database.engine import engine
from database.models import User, Transaction

def set_user(telegram_id: int, first_name: str, last_name: str | None = None):
    """Добавляет пользователя в БД, если его там еще нет"""
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.telegram_id == str(telegram_id)))

        if not user:
            new_user = User(
                telegram_id=str(telegram_id),
                first_name=first_name,
                last_name=last_name
            )
            session.add(new_user)
            session.commit()
            print(f"Новый пользователь {first_name} добавлен в базу!")
        else:
            print(f"Пользователь {first_name} уже есть в базе.")

def add_transaction(telegram_id: int, amount: int, category: str):
    """Добавляет новую транзакцию для пользователя"""
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.telegram_id == str(telegram_id)))
        
        if user:
            new_tx = Transaction(
                user_id=user.id, 
                amount=amount, 
                category=category
            )
            session.add(new_tx)
            session.commit()
            print(f"Транзакция добавлена: {amount} -> {category}")

def get_user_stats(telegram_id: int):
    """Считает сумму трат по категориям для конкретного юзера"""
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.telegram_id == str(telegram_id)))
        
        if not user:
            return None
            
        stmt = (
            select(Transaction.category, func.sum(Transaction.amount))
            .where(Transaction.user_id == user.id)
            .group_by(Transaction.category)
        )
        
        result = session.execute(stmt).all()
        return result

def get_all_transactions(telegram_id: int):
    """Достает полную историю транзакций пользователя"""
    with Session(engine) as session:
        user = session.scalar(select(User).where(User.telegram_id == str(telegram_id)))
        if not user:
            return []
        stmt = select(Transaction).where(Transaction.user_id == user.id).order_by(Transaction.transaction_date)
        return session.scalars(stmt).all()
