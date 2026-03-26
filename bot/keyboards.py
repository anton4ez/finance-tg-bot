from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить расход")],
        [KeyboardButton(text="Статистика"), KeyboardButton(text="График")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие..."
)

categories_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Еда"), KeyboardButton(text="Транспорт")],
        [KeyboardButton(text="Здоровье"), KeyboardButton(text="Супермаркет")],
        [KeyboardButton(text="Коммуналка"), KeyboardButton(text="Развлечения")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите категорию..."
)
