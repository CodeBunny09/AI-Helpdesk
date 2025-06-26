from django.db import models

class Lead(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('prospect', 'Prospect'),
        ('interested', 'Interested'),
        ('customer', 'Customer'),
    ]

    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.name} - {self.phone_number} - {self.status}"

class ChatHistory(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE, related_name='chat_histories')
    sender = models.CharField(max_length=50)  # 'user' or 'bot'
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat with {self.lead.name} at {self.timestamp}"
