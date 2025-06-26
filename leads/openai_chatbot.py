"""
OpenAI helper wrapper using the **v1** Python SDK (>=1.0.0).

Exports
-------
OPENAI_MODEL       – default model name (env-overrideable)
_format_history()  – helper for converting chat history
get_openai_response(prompt, history) – synchronous call
stream_openai_response(prompt, history) – sync generator for streaming
"""

import os
from typing import Iterable, List, Tuple

import openai
from dotenv import load_dotenv

# ---------------------------------------------------------------------
# ENV & CLIENT SETUP
# ---------------------------------------------------------------------
load_dotenv()  # reads .env for OPENAI_API_KEY, OPENAI_MODEL, etc.

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
# Synchronous client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# ---------------------------------------------------------------------
# INTERNAL HELPERS
# ---------------------------------------------------------------------
def _format_history(chat_history: List[Tuple[str, str]] | None) -> List[dict]:
    """Convert list[(user, bot)] → OpenAI messages list."""
    messages: List[dict] = []
    if chat_history:
        for user_msg, bot_msg in chat_history:
            messages.append({"role": "user", "content": user_msg})
            if bot_msg:
                messages.append({"role": "assistant", "content": bot_msg})
    return messages


# ---------------------------------------------------------------------
# PUBLIC FUNCTIONS
# ---------------------------------------------------------------------
def get_openai_response(prompt: str, chat_history=None) -> str:
    """Blocking helper – returns the full assistant reply."""
    messages = _format_history(chat_history) + [{"role": "user", "content": prompt}]
    resp = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
    )
    return resp.choices[0].message.content.strip()


def stream_openai_response(
    prompt: str, chat_history: List[Tuple[str, str]] | None = None
) -> Iterable[str]:
    """Sync generator for streaming chunks (used by non-async UIs)."""
    messages = _format_history(chat_history) + [{"role": "user", "content": prompt}]
    collected = ""
    for chunk in client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
        stream=True,
    ):
        delta = chunk.choices[0].delta.content or ""
        collected += delta
        yield collected
