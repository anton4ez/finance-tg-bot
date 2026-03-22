from database.engine import engine
from database.models import Base

print("Начинаем очистку базы...")
Base.metadata.drop_all(engine)
print("Создаем чистые таблицы заново...")
Base.metadata.create_all(engine)
print("Готово!")
