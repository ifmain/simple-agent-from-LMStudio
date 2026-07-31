from chat_tools import getSimpleAgent
from models.ranking import Rank
from models.planning import Plan
from models.solving import Solve
from models.finalize import Finalize

def to_txt(pydantic_instance):
    return pydantic_instance.model_dump_json(indent=4)

def genPlans(llm, user_prompt, nums=3):
    plan_func = Plan(llm)
    plans_txt = []
    plans_raw = []
    
    for i in range(nums):
        result = plan_func.get_plan(user_prompt)
        if result["data"]:
            plans_txt.append(to_txt(result["data"]))
            plans_raw.append(result["data"].model_dump())
        else:
            print(f"Ошибка при генерации плана {i}: {result['error']}")
            
    return plans_txt, plans_raw

def race(llm, user_prompt, task, ideas_txt, ideas_raw):
    rank_funk = Rank(llm)
    result = rank_funk.get_ideas_race(user_prompt, task, ideas_txt)
    
    if result["error"] or not result["data"]:
        print(f"Ошибка ранжирования: {result['error']}")
        return []

    data_obj = result['data']
    top3ids = data_obj.Top3ids
    top3ranks = data_obj.Top3idsRank
    
    top = []
    # Защита от выхода за пределы списка, если ИИ вернул кривые ID
    for i in range(len(top3ids)):
        idx = top3ids[i]
        if idx < len(ideas_raw):
            top.append({
                'variant': ideas_raw[idx],
                'rank': top3ranks[i]
            })
    return top

def get_formatted_plan(item):
    v = item['variant']
    plan_body = "\n".join([
        "## План",
        f"#### Метрика:\n{v['metrics']}",
        f"#### Архитектура:\n{v['arch']}"
    ])

    steps_out = []
    for step in v["steps"]:
        str_out = [
            f"  - Этап: {step['step']}",
            f"    Описание: {step['description']}",
            "    Исправления:"
        ]
        fixes = step["self_fix"]
        for i in range(len(fixes)):
            str_out.append(f"      {i+1}: {fixes[i]}")
        steps_out.append("\n".join(str_out))
    
    return plan_body, steps_out

def display_final_plan(item, body, steps_list):
    print(f"\n" + "="*20)
    print(f"## Ранг: {item['rank']}")
    print(body)
    
    print(f"#### Этапы ({len(steps_list)})")
    for step_text in steps_list:
        print(step_text)
    print('-' * 20)

def solve_it(llm, plan_body, step_text, context):
    solove_func = Solve(llm) # Новый класс
    result = solove_func.solve(plan_body, step_text, context)
    
    if result["error"] or not result["data"]:
        print(f"Ошибка решения: {result['error']}")
        return ""

    data_obj = result['data']
    solving = data_obj.solving
    solving_reason = data_obj.solving_reason
    solving_selfcorrection = data_obj.solving_selfcorrection

    return (
        f"### Решение\n{solving}\n\n"
        f"### Объяснение\n{solving_reason}\n\n"
        f"### Самокоррекция\n{solving_selfcorrection}"
    )

def ai_solver(llm, user_prompt):
    print("ГЕНЕРАЦИЯ ПЛАНОВ...")
    plans_txt, plans_raw = genPlans(llm, user_prompt, nums=5)
    
    if not plans_raw:
        print("Не удалось сгенерировать ни одного плана.")
        exit()

    task = "Оценка структуры и метрик плана"
    top = race(llm, user_prompt, task, plans_txt, plans_raw)
    
    if not top:
        print("Ошибка при выборе лучшего плана.")
        exit()

    # Берем лучший план (топ 0)
    formatted_body, formatted_steps = get_formatted_plan(top[0])
    display_final_plan(top[0], formatted_body, formatted_steps)
    
    context = ""
    
    # --- ЦИКЛ РЕШЕНИЯ ШАГОВ С РАНЖИРОВАНИЕМ ---
    for i in range(len(formatted_steps)):
        print(f"\n>>> Решаем этап {i+1} из {len(formatted_steps)}...")
        solvings_raw = []
        
        # Генерируем 3 варианта решения для шага
        for j in range(3):
            res = solve_it(llm, formatted_body, formatted_steps[i], context)
            if res:
                solvings_raw.append(res)
        
        if not solvings_raw:
            print(f"Провал на этапе {i+1}.")
            continue

        # Ранжируем эти 3 варианта
        step_task = f"Оцени варианты решения для этапа: {formatted_steps[i]}"
        top_step_solutions = race(llm, user_prompt, step_task, solvings_raw, solvings_raw)

        if top_step_solutions:
            best_solution = top_step_solutions[0]['variant']
            print(f"Выбрано лучшее решение с рангом {top_step_solutions[0]['rank']}")
            print(f"\n\n--- РЕЗУЛЬТАТ ЭТАПА {i+1} ---\n{best_solution}")
        else:
            best_solution = solvings_raw[0]
            print("Ранжирование не удалось, берем первый вариант.")

        # Добавляем только лучшее решение в контекст
        context += f"\n\n--- РЕЗУЛЬТАТ ЭТАПА {i+1} ---\n{best_solution}"

    
    # --- ФИНАЛИЗАЦИЯ ---
    print("\n" + "="*30)
    print("ФОРМИРОВАНИЕ ИТОГОВОГО ОТВЕТА...")
    
    fin_func = Finalize(llm)
    final_res = fin_func.get_final_answer(user_prompt, context)
    
    if final_res["error"] or not final_res["data"]:
        return f"Ошибка при формировании финала: {final_res['error']}"
    else:
        
        return final_res["data"].answer
    return f"Ошибка"

if __name__ == "__main__":
    llm = getSimpleAgent()
    user_prompt = "Напиши стих о осени на 4 четверостишия"
    answer = ai_solver(llm, user_prompt)

    print("\n=== ИТОГОВЫЙ ОТВЕТ (ANSWER) ===")
    print(answer)
    