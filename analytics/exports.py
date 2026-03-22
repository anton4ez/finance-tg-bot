import pandas as pd
import io
from database.models import Transaction

def generate_excel_report(transactions: list[Transaction]) -> io.BytesIO:
    """Превращает список транзакций в Excel-файл в оперативной памяти"""

    data = []
    for t in transactions:
        data.append({
            "ID операции": t.id,
            "Дата и время": t.transaction_date.strftime("%Y-%m-%d %H:%M:%S"),
            "Категория": t.category,
            "Сумма (руб.)": t.amount
        })
        
    df = pd.DataFrame(data)
    buf = io.BytesIO()
    
    with pd.ExcelWriter(buf, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Мои расходы')
    buf.seek(0)
    
    return buf
