import json
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
path = os.path.join(BASE_DIR, "prompt.json")
def load_prompt_template():
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_prompt(template, query, context):
    system_prompt = template["system"]
    user_prompt = template["user"] \
        .replace("{{query}}", query) \
        .replace("{{context}}", context)

    return system_prompt, user_prompt
