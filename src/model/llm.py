from google import genai
from google.genai import types
def ask_gemini(contents: str, system_prompt: str) -> str:
    client = genai.Client(api_key="REMOVED")
    response = client.models.generate_content(model="gemini-2.5-flash", contents=contents, config= types.GenerateContentConfig(system_instruction=system_prompt))
    return response
