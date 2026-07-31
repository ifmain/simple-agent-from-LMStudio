from models_format.solving import SolveIt
from models_format.solving import system_prompts as solving_system_prompts

class Solve:
    def __init__(self, agent):
        self.llm = agent
        
    def solve(self, parse_plan, step, context):
        user_prompt = (
            f"### План решения\n{parse_plan}\n\n"
            f"### Текущее задание:\n{step}\n\n"
            f"### Контекст прошлых решний:\n{context}"
        )
        messages = [
            {"role": "system", "content": solving_system_prompts["SolveIt"]},
            {"role": "user", "content": user_prompt},
        ]

        result = self.llm.formated(messages, SolveIt)
        return result