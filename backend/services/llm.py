import os

from openai import OpenAI


MODEL_NAME = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")


def call_llm(prompt: str, system_role: str = "You are a helpful cybersecurity assistant.") -> str:
    """Calls OpenAI API and returns plain text output."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return ""

    client = OpenAI(api_key=api_key)
    response = client.responses.create(
        model=MODEL_NAME,
        input=[
            {"role": "system", "content": system_role},
            {"role": "user", "content": prompt},
        ],
    )
    return response.output_text.strip()
