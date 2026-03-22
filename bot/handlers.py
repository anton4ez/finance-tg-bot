from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram import F
from analytics.visualizations import create_pie_chart
from analytics.exports import generate_excel_report
from bot.keyboards import categories_kb, main_kb 
from bot.states import TransactionStates
from database.requests import set_user, add_transaction, get_user_stats, get_all_transactions


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
        "Отлично! Теперь выбери категорию:", 
        reply_markup=categories_kb
    )
    await state.set_state(TransactionStates.waiting_for_category)


@router.message(TransactionStates.waiting_for_category)
async def process_category(message: Message, state: FSMContext):
    data = await state.get_data()
    amount = data['amount']
    category = message.text

    add_transaction(
        telegram_id=message.from_user.id,
        amount=amount,
        category=category
    )

    await message.answer(
        f"Успешно записано!\nСумма: {amount}\nКатегория: {category}",
        reply_markup=main_kb
    )
    await state.clear()

@router.message(Command("stats"))
@router.message(F.text == "Статистика")
async def cmd_stats(message: Message):
    stats = get_user_stats(message.from_user.id)
    
    if not stats:
        await message.answer("У тебя пока нет никаких трат. Напиши /add, чтобы добавить первую!")
        return
        
    text = "📊 <b>Твоя статистика расходов:</b>\n\n"
    total_sum = 0
    
    for category, amount in stats:
        text += f"{category}: {amount} руб.\n"
        total_sum += amount
        
    text += f"\n<b>Всего потрачено:</b> {total_sum} руб."
    
    await message.answer(text, parse_mode="HTML")

@router.message(Command("chart"))
@router.message(F.text == "График")
async def cmd_chart(message: Message):
    stats = get_user_stats(message.from_user.id)
    
    if not stats:
        await message.answer("Нет данных для графика. Добавь траты через /add!")
        return
        
    chart_buffer = create_pie_chart(stats)
    photo = BufferedInputFile(chart_buffer.read(), filename="chart.png")
    await message.answer_photo(photo=photo, caption="Твоя финансовая картина:")

@router.message(Command("export"))
async def cmd_export(message: Message):
    transactions = get_all_transactions(message.from_user.id)
    
    if not transactions:
        await message.answer("У тебя пока нет трат для выгрузки.")
        return
        
    await message.answer("Формирую отчет, секундочку...")
    
    excel_buffer = generate_excel_report(transactions)
    document = BufferedInputFile(excel_buffer.read(), filename="My_Expenses.xlsx")
    
    await message.answer_document(document=document, caption="Твоя полная выгрузка расходов готова!")
