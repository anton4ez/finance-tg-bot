from sentence_transformers import SentenceTransformer, util
import torch


model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

categories = [
    "Еда, продукты, ресторан, фастфуд, хавчик, перекус, обед, макдак",
    "Транспорт, такси, машина, бензин, метро, автобус, заправка",
    "Здоровье, больница, медицина, аптека, таблетки, врач",
    "Коммуналка, ЖКХ, отопление, свет, вода, интернет, связь, тариф",
    "Супермаркет, магазин, товары, пятерочка, магнит, перекресток, ашан, дикси",
    "Развлечения, аттракционы, парк, батуты, боулинг, кино"
]

embeddings = model.encode(categories)

def predict_category(user_input: str) -> str | None:
    """
    Принимает текст расхода от юзера, возвращает название категории 
    или None, если уверенность модели слишком низкая.
    """
    user_embadding = model.encode(user_input)

    scores = util.cos_sim(user_embadding, embeddings)[0]
    best_idx = int(torch.argmax(scores).item())
    best_score = scores[best_idx].item()

    if best_score < 0.3:
        return None

    matched_category = categories[best_idx].split(',')[0]

    return matched_category
