import os, json, logging

base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
config_path = os.path.join(base_dir, "config.json")

with open(config_path, encoding='utf-8') as f:
    raw_config = json.load(f)

base_url = raw_config.get("server")
api_key = raw_config.get("api_key")
temperature = raw_config.get("temperature")
model = raw_config.get("model")
is_debug = raw_config.get("is_debug")
is_test = raw_config.get("is_test")
user_lang = raw_config.get("lang")

'''
if is_debug:
    level = logging.DEBUG
else:
    level = logging.INFO

logging.basicConfig(
    level=level,
    format='%(levelname)s: %(message)s'
)
'''