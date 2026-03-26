from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram import F
from bot.keyboards import categories_kb, main_kb 
from bot.states import TransactionStates
from database.requests import add_transaction, get_user_stats
from services.categories import predict_category


router = Router()

@router.message(Command("add"))
@router.message(F.text == "Добавить расход")
async def cmd_add(message: Message, state: FSMContext):
    await message.answer("Введи сумму расхода (только число):")
    await state.set_state(TransactionStates.waiting_for_amount)

@router.message(TransactionStates.waiting_for_amount)
async def process_amount(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Ошибка! Пожалуйста, введи только число (например, 500):")
        return

    await state.update_data(amount=int(message.text))

    await message.answer(
        "Отлично! Напиши, на что пошли деньги (например, 'шаурма' или 'такси'), либо выбери категорию кнопкой:", 
        reply_markup=categories_kb
    )

    await state.set_state(TransactionStates.waiting_for_category)

@router.message(TransactionStates.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data['amount']
    
    category = predict_category(message.text)

    if category:
        add_transaction(
            telegram_id=message.from_user.id,
            amount=amount,
            category=category
        )

        success_text = (
            f"<b>Успешно записано!</b>\n\n"
            f"Сумма: {amount} руб.\n"
            f"Категория: {category}"
        )

        await message.answer(success_text, reply_markup=main_kb, parse_mode="HTML")
        await state.clear()

    else:
        await message.answer(
            "Не уверен, куда это отнести(\nПожалуйста, уточни, выбрав категорию на клавиатуре:", 
            reply_markup=categories_kb
        )

@router.message(Command("stats"))
@router.message(F.text == "Статистика")
async def cmd_stats(message: Message):
    stats = get_user_stats(message.from_user.id)
    
    if not stats:
        await message.answer("У тебя пока нет никаких трат. Напиши /add, чтобы добавить первую!")
        return
        
    text = "<b>Твоя статистика расходов:</b>\n\n"
    total_sum = 0
    
    for category, amount in stats:
        text += f"{category}: {amount} руб.\n"
        total_sum += amount
        
    text += f"\n<b>Всего потрачено:</b> {total_sum} руб."
    
    await message.answer(text, parse_mode="HTML")
