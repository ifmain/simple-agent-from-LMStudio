from pydantic import BaseModel

class RankIt(BaseModel):
    rank: float
    reason: str

class RaceIt(BaseModel):
    Top3ids: list[int]
    Top3idsRank: list[float]
    reason_best: str
    reason_worst: str

system_prompts = {
    "RankIt": (
        "rank — это число в пределах от 0 до 1, где 0 — худшее, а 1 — лучшее. "
        "Дай оценку в (rank). Объясни почему. "
        "У тебя в блоке пользователя будут входные данные: `Основной запрос`, `Текущая задача`, `Предложение по этой задаче`. Используй их."
    ),

    "RaceIt": (
        "rank — это число в пределах от 0 до 1, где 0 — худшее, а 1 — лучшее. "
        "Выведи топ-3 ID из предложенных вариантов (Top3ids). "
        "Выведи ИМЕННО ДЛЯ ЭТИХ 3 ids их ранг (Top3idsRank). "
        "Дай ответ — почему именно эти топ-3 ты выбрал и почему дал именно такой ранг (reason_best). "
        "Дай ответ — почему ты не выбрал остальные варианты, чем они тебя не устроили (reason_worst). "
        "Учти — в Top3idsRank ты даёшь ответ в list of float, а не dict str: float или dict int: float."
    )
}