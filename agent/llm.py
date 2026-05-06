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
        model="llama-3.3-70b-versatile",
        max_tokens=4096,
        messages=[
            {"role": "system", "content": system},
            *messages
        ]
    )
    return response.choices[0].message.content