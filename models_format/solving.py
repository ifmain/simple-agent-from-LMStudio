from typing import List
from pydantic import BaseModel, Field

class SolveIt(BaseModel):
    solving: str
    solving_reason: str
    solving_selfcorrection: str

system_prompts = {
    "SolveIt": (
        "Ты должен выполнить задачу в полном объёме, которого требует текущий этап, и вывести ответ в solving. "
        "Ты должен обосновать своё решение в solving_reason. "
        "В solving_selfcorrection ты должен ясно сказать, соблюдал ли ты самокоррекцию и как, а также дать объяснение почему."
    )
}