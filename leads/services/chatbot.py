from ..models import Lead, ChatHistory
from ..openai_chatbot import get_openai_response

def get_next_lead():
    """
    Fetch the next available lead with status 'pending'.
    """
    return Lead.objects.filter(status='pending').first()


def simulate_chat_with_lead(lead):
    """
    Dummy function to simulate a chatbot conversation with a lead.
    Saves both user input and bot response in ChatHistory.
    """
    try:
        # Example dummy user message
        user_message = f"Hello {lead.name}, are you interested in our services?"

        # Get OpenAI response (calls the backend logic)
        bot_response = get_openai_response(user_message)

        # Save User Message
        ChatHistory.objects.create(
            lead=lead,
            sender='user',
            message=user_message
        )

        # Save Bot Response
        ChatHistory.objects.create(
            lead=lead,
            sender='bot',
            message=bot_response
        )

        # Update lead status if needed
        # Example: Move pending leads to 'prospect' after chat
        if lead.status == 'pending':
            lead.status = 'prospect'
            lead.save()

    except Exception as e:
        print(f"Error during chat simulation: {e}")
