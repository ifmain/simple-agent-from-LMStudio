from models_format.finalize import FinalizeIt
from models_format.finalize import system_prompts as finalize_system_prompts

class Finalize:
    def __init__(self, agent):
        self.llm = agent
        
    def get_final_answer(self, user_prompt, context):
        prompt = (
            f"### Исходный запрос пользователя:\n{user_prompt}\n\n"
            f"### Выполненные шаги и решения (Контекст):\n{context}\n\n"
            f"Сформируй итоговый ответ."
        )
        messages = [
            {"role": "system", "content": finalize_system_prompts["FinalizeIt"]},
            {"role": "user", "content": prompt},
        ]

        result = self.llm.formated(messages, FinalizeIt)
        return result