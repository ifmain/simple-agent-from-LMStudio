from openai import OpenAI
from config import config
import logging
from config import lang_settings
import re

class ChatPrepare:
    def __init__(self, base_url="http://localhost:1234/v1", api_key="lm-studio", model="qwen3.5-9b-claude-4.6-opus-reasoning-distilled-v2"):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model = model
        self.temperature = config.temperature

    def answer(self, messages):
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=self.temperature
            )

            message_obj = response.choices[0].message
            text_content = message_obj.content or ""
            reasoning = getattr(message_obj, 'reasoning_content', None) or ""

            return {
                "reasoning": reasoning.strip(),
                "text": text_content.strip(),
                "error": None
            }

        except Exception as e:
            return {
                "reasoning": "",
                "text": "",
                "error": str(e)
            }

    def formated(self, messages, response_format_class, attempts=3):
        fields = response_format_class.model_fields.keys()
        fields_str = ", ".join(fields)
        
        old_sys = [m['content'] for m in messages if m["role"] == "system"]

        # Исправлено: объединяем всё в одну строку без запятых (кортежей)
        content_str = (
            f"{lang_settings.sys_prefix} "
            f"Твоя задача — выдать JSON объект строго по классу {response_format_class.__name__}. "
            f"Обязательные поля: {fields_str}. "
            f"Не пиши никаких пояснений, только чистый JSON.\n\n"
            f"{'\n\n'.join(old_sys)}"
        )

        sys_msg = {
            "role": "system", 
            "content": content_str
        }
        
        new_messages = [sys_msg] + [m for m in messages if m["role"] != "system"]

        out_obj = {}
        text_content = "" # Инициализируем заранее, чтобы не было UnboundLocalError
        for i in range(attempts):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=new_messages,
                    temperature=self.temperature
                )

                message_obj = response.choices[0].message
                text_content = message_obj.content or ""
                
                '''if "```" in text_content:
                    text_content = text_content.split("```")[-2].split("json")[-1].strip()
                '''

                if "```" in text_content:
                    match = re.search(r'\{.*\}', text_content, re.DOTALL)
                    if match:
                        text_content = match.group(0)

                reasoning = getattr(message_obj, 'reasoning_content', None) or ""
                parsed_data = response_format_class.model_validate_json(text_content.strip())

                return {
                    "reasoning": reasoning.strip(),
                    "data": parsed_data,
                    "error": None
                }

            except Exception as e:
                logging.debug(f"attempts {i+1}/{attempts}: error {e}")
                out_obj = {"data": None, "error": f"Request or Parsing failed: {e}. Raw content: {text_content}"}
        return out_obj


def getSimpleAgent():
    return ChatPrepare(
        base_url=config.base_url,
        model=config.model,
        api_key=config.api_key
    )