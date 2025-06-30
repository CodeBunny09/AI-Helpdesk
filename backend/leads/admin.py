from django.contrib import admin
from .models import Lead, Conversation, Text, HotelRoom

admin.site.register(Lead)
admin.site.register(Conversation)
admin.site.register(Text)
admin.site.register(HotelRoom)
