# === FILE: backend/leads/models.py ===
from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
        ('follow_up', 'Follow Up'),
    ]

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    last_contacted = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name


class HotelRoom(models.Model):
    ROOM_TYPES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe')
    ]

    room_number = models.CharField(max_length=10)
    room_type = models.CharField(max_length=10, choices=ROOM_TYPES)
    is_available = models.BooleanField(default=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField(blank=True)
    max_occupancy = models.IntegerField(default=2)
    amenities = models.TextField(blank=True)

    def __str__(self):
        return f"{self.room_type.title()} Room {self.room_number}"


class Conversation(models.Model):
    CONVO_TYPE = [
        ("chat", "Chat"),
        ("call", "Call")
    ]
    CONVO_TAGS = [
        ("sales", "Sales"),
        ("issue", "Issue"),
        ("request", "Request"),
        ("misc", "Misc")
    ]

    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name="conversations")
    is_inbound = models.BooleanField(default=False)
    conversation_type = models.CharField(max_length=10, choices=CONVO_TYPE)
    tag = models.CharField(max_length=20, choices=CONVO_TAGS, blank=True)
    outcome = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    started_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.conversation_type.title()} - {self.lead.name} ({'Inbound' if self.is_inbound else 'Outbound'})"


class Text(models.Model):
    SENDER_CHOICES = [
        ("user", "User"),
        ("bot", "Bot")
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="texts")
    sender = models.CharField(max_length=10, choices=SENDER_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender.title()}: {self.content[:40]}..."
