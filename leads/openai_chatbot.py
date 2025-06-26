import openai
import os
from dotenv import load_dotenv
from typing import Iterable, List, Tuple


load_dotenv()  # Load your .env file with OPENAI_API_KEY

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_openai_response(prompt, chat_history=None):
    """
    Sends the user prompt and chat history to OpenAI and returns the response.

    Args:
        prompt (str): User input
        chat_history (list): Previous chat history (optional)

    Returns:
        str: Assistant's reply
    """
    try:
        messages = []

        # Add chat history if available
        if chat_history:
            for user_msg, bot_msg in chat_history:
                messages.append({"role": "user", "content": user_msg})
                messages.append({"role": "assistant", "content": bot_msg})

        # Add latest user prompt
        messages.append({"role": "user", "content": prompt})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4" if available
            messages=messages,
            temperature=0.7
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"OpenAI Error: {str(e)}"


def stream_openai_response(
    prompt: str, chat_history: List[Tuple[str, str]] | None = None
) -> Iterable[str]:
    """
    Generator yielding content chunks for Gradio streaming UI.
    """
    messages = _format_history(chat_history) + [{"role": "user", "content": prompt}]
    resp = openai.ChatCompletion.create(
        model=OPENAI_MODEL,
        messages=messages,
        stream=True,
        temperature=0.7,
    )
    collected = ""
    for chunk in resp:
        delta = chunk.choices[0].delta.get("content", "")
        collected += delta
        yield collected
