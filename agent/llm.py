import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(messages: list, system: str) -> str:
    """
    Send message history to Groq and return the text response.

    Args:
        messages: Full conversation history [{"role": ..., "content": ...}]
        system:   The system prompt string

    Returns:
        The assistant's reply as a plain string
    """
    response = client.chat.completions.create(
        model="qwen/qwen3.6-27b",
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system},
            *messages
        ]
    )
    return response.choices[0].message.content
