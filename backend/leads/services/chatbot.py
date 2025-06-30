from ..models import Lead, Conversation, Text
from ..openai_chatbot import get_openai_response
import openai


def get_next_lead():
    return Lead.objects.filter(status='pending').first()


def simulate_chat_with_lead(lead):
    try:
        user_message = f"Hello {lead.name}, are you interested in booking a room with us?"
        bot_response = get_openai_response(user_message)

        # Create conversation and turns
        conversation = Conversation.objects.create(
            lead=lead,
            is_inbound=False,
            conversation_type="chat"
        )
        Text.objects.create(conversation=conversation, sender="user", content=user_message)
        Text.objects.create(conversation=conversation, sender="bot", content=bot_response)

        # Collate conversation so far
        transcript = f"User: {user_message}\nBot: {bot_response}"

        # GPT prompt for summarization and tagging
        system_prompt = (
            "You are a CRM assistant. Given the following conversation, generate:\n"
            "1. A tag: one of 'sales', 'issue', 'request', or 'misc'.\n"
            "2. An outcome (short string).\n"
            "3. A brief summary of the conversation.\n"
            "Format:\n"
            "Tag: <tag>\nOutcome: <outcome>\nNotes: <summary>"
        )

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": transcript}
            ]
        )

        summary_text = completion['choices'][0]['message']['content']

        # Extract fields from GPT result
        lines = summary_text.strip().splitlines()
        tag = next((line.split(":")[1].strip() for line in lines if line.lower().startswith("tag:")), "")
        outcome = next((line.split(":")[1].strip() for line in lines if line.lower().startswith("outcome:")), "")
        notes = next((line.split(":", 1)[1].strip() for line in lines if line.lower().startswith("notes:")), "")

        # Apply to conversation
        conversation.tag = tag
        conversation.outcome = outcome
        conversation.notes = notes
        conversation.save()

        # Update lead
        if lead.status == 'pending':
            lead.status = 'interested'
            lead.save()

    except Exception as e:
        print(f"Error during chat simulation: {e}")
