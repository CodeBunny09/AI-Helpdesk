import gradio as gr
import openai
import os

# ✅ Set your OpenAI API key (or use env var)
openai.api_key = os.getenv("OPENAI_API_KEY")  # Or hardcode your key here (Not recommended for prod)

def chat_openai(user_input, chat_history):
    try:
        # Format chat history for OpenAI API
        messages = [{"role": "system", "content": "You are a helpful assistant."}]
        for user, bot in chat_history:
            messages.append({"role": "user", "content": user})
            messages.append({"role": "assistant", "content": bot})

        messages.append({"role": "user", "content": user_input})

        # Call OpenAI API (ChatCompletion)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or "gpt-4o" or "gpt-4"
            messages=messages,
        )

        bot_reply = response.choices[0].message.content.strip()
        chat_history.append((user_input, bot_reply))
        return "", chat_history

    except Exception as e:
        return "", chat_history + [(user_input, f"[Error]: {str(e)}")]

# ✅ Build Gradio Chat UI
with gr.Blocks() as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox(placeholder="Ask me something...")

    state = gr.State([])

    msg.submit(chat_openai, [msg, state], [msg, chatbot, state])

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
