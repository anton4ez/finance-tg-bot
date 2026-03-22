from database.engine import engine
from database.models import Base


print("Подключаемся к базе данных...")

Base.metadata.create_all(engine)

print("Таблицы успешно созданы!")
