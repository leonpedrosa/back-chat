from django.contrib import admin
from api.models import *

class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'recipient', 'text', 'timestamp']

admin.site.register(Message, MessageAdmin)