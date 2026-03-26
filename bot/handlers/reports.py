from aiogram import Router
from aiogram.types import Message, BufferedInputFile
from aiogram.filters import Command
from aiogram import F
from analytics.visualizations import create_pie_chart
from analytics.exports import generate_excel_report
from database.requests import get_user_stats, get_all_transactions


router = Router()

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
