import matplotlib
import matplotlib.pyplot as plt
import io


matplotlib.use('Agg')

def create_pie_chart(stats: list[tuple[str, int]]) -> io.BytesIO:
    """Создает круговую диаграмму из списка кортежей [(Категория, Сумма), ...]"""
    
    labels = [item[0] for item in stats]
    sizes = [item[1] for item in stats]
    
    fig, ax = plt.subplots(figsize=(6, 6))
    
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140, 
           colors=matplotlib.colormaps['Paired'].colors)
           
    ax.set_title("Структура твоих расходов")
    buf = io.BytesIO()
    
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    
    buf.seek(0)
    
    return buf
