import os
import openai
from openai import OpenAI
from app.core.config import settings

client = OpenAI(api_key=settings.openai_api_key)

def chat_completion(messages, model="gpt-4", temperature=0.4) -> str:
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content.strip()
