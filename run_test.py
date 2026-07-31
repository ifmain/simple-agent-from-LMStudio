from chat_tools import getSimpleAgent
from config import config
import logging

from models_format.test import CalendarEvent
from models_format.naming import NameIt, TitleIt
from models_format.naming import system_prompts as naming_system_prompts

from models.ranking import Rank
from models.planning import Plan


# Body
class UnitTests:
    def __init__(self, agent):
        self.llm = agent

    def simple_test(self):
        messages = [
            {"role": "system", "content": "You answer only in rhymes."},
            {"role": "user", "content": "What is your favorite color?"}
        ]

        result = self.llm.answer(messages)

        if not result["error"]:
            print("\n" + "="*20 + " SIMPLE TEST " + "="*20)
            if result["reasoning"]:
                print("=== РАССУЖДЕНИЯ ===")
                print(result["reasoning"])

            print("\n=== ОТВЕТ ===")
            print(result["text"])
        else:
            logging.debug(f"ПРОИЗОШЛА ОШИБКА: {result['error']}")

    def formated_test(self):
        messages = [
            {"role": "system", "content": "You answer only in rhymes."},
            {
                "role": "user",
                "content": "Alice and Bob are going to a science fair on Friday. Напиши стих для них на русском",
            },
        ]

        result = self.llm.formated(messages, CalendarEvent)

        if not result["error"]:
            print("\n" + "="*20 + " FORMATTED TEST " + "="*20)
            if result["reasoning"]:
                print("=== РАССУЖДЕНИЯ ===")
                print(result["reasoning"])

            print("\n=== ОТВЕТ (Pydantic Object) ===")
            print(result["data"])
        else:
            logging.debug(f"ПРОИЗОШЛА ОШИБКА: {result['error']}")
    
    def name_it_test(self):
        with open("data/Структурирование_папок_в_проекте_2026-04-26_022225.md", encoding='utf-8') as f:
            data = f.read()
        
        messages = [
            {"role": "system", "content": naming_system_prompts["NameIt"]},
            {
                "role": "user",
                "content": data,
            },
        ]

        result = self.llm.formated(messages, NameIt)

        if not result["error"]:
            print("\n" + "="*20 + " FORMATTED TEST " + "="*20)
            if result["reasoning"]:
                print("=== РАССУЖДЕНИЯ ===")
                print(result["reasoning"])

            print("\n=== ОТВЕТ (Pydantic Object) ===")
            print(result["data"])
        else:
            logging.debug(f"ПРОИЗОШЛА ОШИБКА: {result['error']}")

    def rank_test(self):
        r = Rank(self.llm)
        user_prompt = "Напиши стих о осени"
        task = "Сосавление рифмы для слова разная"
        idea = "прекрасная"
        result = r.get_idea_rank(user_prompt, task, idea)

        if not result["error"]:
            print("\n" + "="*20 + " FORMATTED TEST " + "="*20)
            if result["reasoning"]:
                print("=== РАССУЖДЕНИЯ ===")
                print(result["reasoning"])

            print("\n=== ОТВЕТ (Pydantic Object) ===")
            print(result["data"])
        else:
            logging.debug(f"ПРОИЗОШЛА ОШИБКА: {result['error']}")
    
    def race_test(self):
        r = Rank(self.llm)
        user_prompt = "Напиши стих о осени"
        task = "Составление рифмы для слова разная"
        ideas = ["прекрасная", "алая", "белая", "синяя", "простая", "внимательная"]
        result = r.get_ideas_race(user_prompt, task, ideas)

        if not result["error"]:
            print("\n" + "="*20 + " FORMATTED TEST " + "="*20)
            if result["reasoning"]:
                print("=== РАССУЖДЕНИЯ ===")
                print(result["reasoning"])

            print("\n=== ОТВЕТ (Pydantic Object) ===")
            print(result["data"])
        else:
            logging.debug(f"ПРОИЗОШЛА ОШИБКА: {result['error']}")
    
    
    def plan_test(self):
        r = Plan(self.llm)
        user_prompt = "Напиши стих о осени"
        result = r.get_plan(user_prompt)

        if not result["error"]:
            print("\n" + "="*20 + " FORMATTED TEST " + "="*20)
            if result["reasoning"]:
                print("=== РАССУЖДЕНИЯ ===")
                print(result["reasoning"])

            print("\n=== ОТВЕТ (Pydantic Object) ===")
            print(result["data"])
        else:
            logging.debug(f"ПРОИЗОШЛА ОШИБКА: {result['error']}")
    



# Функции
def testing():
    if config.is_test:
        logging.info("Режим тестирования")
        testes = UnitTests(llm)

        #testes.simple_test()
        #testes.formated_test()
        #testes.name_it_test()
        #testes.rank_test()
        #testes.race_test()
        testes.plan_test()
        exit()

# Body
if __name__ == "__main__":
    llm = getSimpleAgent()
    testing()