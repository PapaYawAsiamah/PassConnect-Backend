from datetime import timezone
from django.db import models
from django.contrib.auth.models import User

class Event(models.Model):
    title = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    deadline_for_registration = models.DateField()
    max_participants = models.IntegerField()
    image = models.ImageField(upload_to='event_images/')
    # image = models.CharField(max_length=255)
    description = models.TextField()  # Added description field
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_events')
    participants = models.ManyToManyField(User, related_name='registered_events', blank=True)

    @property
    def is_passed(self):
        return self.date < timezone.now().date()

    def __str__(self):
        return self.title
