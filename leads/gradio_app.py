"""
Async streaming Gradio interface using OpenAI v1 **async** client.
Run standalone with:
    python -m leads.gradio_app
"""

import asyncio
from typing import AsyncGenerator, List, Tuple

import gradio as gr
import openai

from .openai_chatbot import OPENAI_MODEL, _format_history

# Async client
aclient = openai.AsyncOpenAI()  # picks up OPENAI_API_KEY from env


# ---------------------------------------------------------------------
# OPENAI STREAMING
# ---------------------------------------------------------------------
async def _openai_stream(
    prompt: str, chat_history: List[Tuple[str, str]] | None
) -> AsyncGenerator[str, None]:
    """Yield incremental assistant text chunks (async)."""
    messages = _format_history(chat_history) + [{"role": "user", "content": prompt}]
    collected = ""
    async for chunk in await aclient.chat.completions.create(
        model=OPENAI_MODEL,
        messages=messages,
        temperature=0.7,
        stream=True,
    ):
        delta = chunk.choices[0].delta.content or ""
        collected += delta
        yield collected


# ---------------------------------------------------------------------
# GRADIO CALLBACK
# ---------------------------------------------------------------------
async def respond(user_message: str, chat_history):
    """
    Async callback for Gradio.
    Yields multiple times so UI streams live tokens.
    """
    formatted_history = [(u, b) for u, b in chat_history]

    partial_reply = ""
    async for new_text in _openai_stream(user_message, formatted_history):
        partial_reply = new_text
        new_state = chat_history + [(user_message, partial_reply)]
        yield "", new_state, new_state

    final_state = chat_history + [(user_message, partial_reply)]
    yield "", final_state, final_state


# ---------------------------------------------------------------------
# GRADIO UI
# ---------------------------------------------------------------------
def launch_gradio_chat():
    with gr.Blocks(title="GPT-4o B2B Sales Assistant (Streaming)") as demo:
        gr.Markdown("### Multilingual Sales Outreach Chatbot")
        chatbot = gr.Chatbot(height=450)
        txt = gr.Textbox(placeholder="Type your message…")
        state = gr.State([])

        txt.submit(respond, [txt, state], [txt, chatbot, state])

    # Must enable queue for async generators
    demo = demo.queue()
    return demo


# Allow quick standalone run
if __name__ == "__main__":
    launch_gradio_chat().launch(server_name="0.0.0.0", server_port=7860, share=False)
