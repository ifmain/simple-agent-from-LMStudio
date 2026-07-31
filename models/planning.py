

from models_format.planning import PlanIt
from models_format.planning import system_prompts as planning_system_prompts

class Plan:
    def __init__(self, agent):
        self.llm = agent
    def get_plan(self, user_prompt):
        messages = [
            {"role": "system", "content": planning_system_prompts["PlanIt"]},
            {
                "role": "user",
                "content": user_prompt,
            },
        ]

        result = self.llm.formated(messages, PlanIt)

        return result
