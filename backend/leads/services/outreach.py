"""
Simple lead-outreach loop for the prototype demo.

Workflow
--------
1. Fetch every Lead with status="pending".
2. Build a short sales prompt and send it to OpenAI.
3. Log the Q&A into Conversation + Text.
4. Ask OpenAI to classify the outcome.
5. Update Lead.status + last_contacted.
"""

from typing import List
from django.utils import timezone

from leads.models import Lead, Conversation, Text
from leads.openai_chatbot import get_openai_response


SYSTEM_TEMPLATE = (
    "You are an AI sales concierge calling on behalf of the Royal Vista 5-Star Hotel. "
    "Politely greet {name}, explain current room promotions, and ask if they are interested."
)

CLASSIFY_TEMPLATE = (
    "Based on this transcript, return ONE WORD from: interested, not_interested, follow_up.\n\n"
    "Transcript:\n{transcript}\n\nONE WORD:"
)


def _simulate_chat(lead: Lead) -> str:
    """
    Run a single prompt–response interaction and return the classified status.
    """
    prompt = SYSTEM_TEMPLATE.format(name=lead.name)
    bot_reply = get_openai_response(prompt)

    # Create a conversation and save both turns
    conversation = Conversation.objects.create(
        lead=lead,
        is_inbound=False,
        conversation_type="chat"
    )
    Text.objects.create(conversation=conversation, sender="user", content=prompt)
    Text.objects.create(conversation=conversation, sender="bot", content=bot_reply)

    # Ask GPT to classify the call outcome
    classify_prompt = CLASSIFY_TEMPLATE.format(
        transcript=f"User: {prompt}\nAssistant: {bot_reply}"
    )
    outcome = get_openai_response(classify_prompt).lower().strip()

    # Map to expected Lead.status values
    if "interested" in outcome:
        return "interested"
    elif "not" in outcome:
        return "not_interested"
    else:
        return "follow_up"


def run_outreach() -> List[int]:
    """
    Loop over all pending leads.
    Returns list of lead IDs that were processed.
    """
    processed: List[int] = []

    for lead in Lead.objects.filter(status="pending"):
        new_status = _simulate_chat(lead)
        lead.status = new_status
        lead.last_contacted = timezone.now()
        lead.save(update_fields=["status", "last_contacted"])
        processed.append(lead.id)

    return processed
