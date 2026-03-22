from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


categories_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Еда"), KeyboardButton(text="Транспорт")],
        [KeyboardButton(text="Развлечения"), KeyboardButton(text="Супермаркет")],
        [KeyboardButton(text="Коммуналка"), KeyboardButton(text="Другое")],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите категорию..."
)

main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Добавить расход")],
        [KeyboardButton(text="Статистика"), KeyboardButton(text="График")],
        [KeyboardButton(text="Отмена")]
    ],
    resize_keyboard=True,
    input_field_placeholder="Выбери действие..."
)
