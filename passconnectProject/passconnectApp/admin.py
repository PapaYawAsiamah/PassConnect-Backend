from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'venue', 'date', 'start_time', 'end_time', 'created_by')
    search_fields = ('title', 'venue', 'created_by__username')
    list_filter = ('date', 'venue')
    ordering = ('-date',)
    fields = ('title', 'venue', 'date', 'start_time', 'end_time', 'deadline_for_registration', 'max_participants', 'description', 'image', 'created_by', 'participants')  # Added max_participants field
