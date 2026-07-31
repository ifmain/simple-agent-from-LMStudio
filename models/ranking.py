

from models_format.ranking import RankIt, RaceIt
from models_format.ranking import system_prompts as ranking_system_prompts

class Rank:
    def __init__(self, agent):
        self.llm = agent
    def get_idea_rank(self, user_prompt, task, idea):
        data = (
            f"### Основой запрос: {user_prompt}.\n"
            f"### Текущая задача: {task}.\n"
            f"### Предложение по этой задаче: {idea}.\n"
            f"\n\n"
            f"Тебе нужно дать ранг для предложение по этой задачи"
        )
        messages = [
            {"role": "system", "content": ranking_system_prompts["RankIt"]},
            {
                "role": "user",
                "content": data,
            },
        ]

        result = self.llm.formated(messages, RankIt)

        return result

    def get_ideas_race(self, user_prompt, task, ideas):
        ideas_text = ""
        for i in range(len(ideas)):
            ideas_text+=f"ID: {i}. Предложение: {ideas[i]}\n"

        data = (
            f"### Основой запрос: {user_prompt}.\n"
            f"### Текущая задача: {task}.\n"
            f"### Предложения по этой задаче:\n"
            f"{ideas_text}"
            f"\n\n"
            f"Тебе нужно дать ранг для предложение по этой задачи"
        )
        messages = [
            {"role": "system", "content": ranking_system_prompts["RaceIt"]},
            {
                "role": "user",
                "content": data,
            },
        ]

        result = self.llm.formated(messages, RaceIt)

        return result