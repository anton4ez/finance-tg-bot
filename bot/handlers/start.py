from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from bot.keyboards import main_kb 
from database.requests import set_user


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    set_user(
        telegram_id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )

    await message.answer(
        f"Привет, {message.from_user.first_name}!\n"
        "Я твой финансовый бот-аналитик. Ты успешно зарегистрирован в моей базе!",
        reply_markup=main_kb
    )

@router.message(StateFilter('*'), Command("cancel"))
@router.message(StateFilter('*'), F.text.lower().in_(['отмена', 'отменить']))
async def cancel_handler(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state is None:
        return
        
    await state.clear()

    await message.answer("Действие отменено. Возвращаемся в главное меню.", reply_markup=main_kb)
