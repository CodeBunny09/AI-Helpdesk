"""
Gradio UI – AI Text Chat Interface Only.
"""

import gradio as gr
import openai
from typing import List, Tuple

from .openai_chatbot import OPENAI_MODEL, _format_history

aclient = openai.AsyncOpenAI()


async def txt_reply(user: str, hist: List[Tuple[str, str]]):
    acc = ""
    msgs = _format_history(hist) + [{"role": "user", "content": user}]
    response = await aclient.chat.completions.create(
        model=OPENAI_MODEL, messages=msgs, stream=True
    )
    async for part in response:
        acc += part.choices[0].delta.content or ""
        yield "", hist + [(user, acc)], hist + [(user, acc)]


def launch_gradio_chat():
    with gr.Blocks(title="AI Text Assistant") as demo:
        gr.Markdown("### 💬 Type to Chat")
        chat = gr.Chatbot(height=450)
        inp = gr.Textbox(placeholder="Type your message here…")
        st = gr.State([])

        inp.submit(txt_reply, [inp, st], [inp, chat, st])

    return demo.queue()


if __name__ == "__main__":
    launch_gradio_chat().launch(server_name="0.0.0.0", server_port=7860, share=False)
