import gradio as gr
from .openai_chatbot import get_openai_response, stream_openai_response

def respond(user_message: str, chat_history):
    """
    Stream tokens back to the UI.

    Returns THREE outputs to match the submit() call:
      1. The (cleared) textbox value
      2. The displayed chatbot history
      3. The internal state object
    """
    from .openai_chatbot import stream_openai_response

    formatted_history = [(usr, bot) for usr, bot in chat_history]
    bot_stream = stream_openai_response(user_message, formatted_history)

    partial_reply = ""
    for new_text in bot_stream:
        partial_reply = new_text
        new_state = chat_history + [(user_message, partial_reply)]
        yield "", new_state, new_state

    final_state = chat_history + [(user_message, partial_reply)]
    yield "", final_state, final_state


def chat_interface(user_input, chat_history):
    """
    Handles chat interactions using OpenAI API.
    """
    bot_reply = get_openai_response(user_input, chat_history)
    chat_history.append((user_input, bot_reply))
    return "", chat_history

def launch_gradio_chat():
    with gr.Blocks(title="GPT-4o B2B Sales Assistant") as demo:
        gr.Markdown("### Multilingual Sales Outreach Chatbot")
        chatbot = gr.Chatbot(height=450)
        msg = gr.Textbox(placeholder="Start typing…")

        state = gr.State([])

        msg.submit(
            fn=respond,
            inputs=[msg, state],
            outputs=[msg, chatbot, state],
        )

    # demo.queue()
    return demo
