from django.core.management.base import BaseCommand
from leads.services.chatbot import get_next_lead, simulate_chat_with_lead

class Command(BaseCommand):
    help = 'Simulates a chatbot conversation with the next available lead.'

    def handle(self, *args, **kwargs):
        lead = get_next_lead()
        if lead:
            simulate_chat_with_lead(lead)
        else:
            self.stdout.write(self.style.WARNING("🚫 No pending leads found."))
