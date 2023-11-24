# Create your models here.
from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField(blank=True, null=True)
    audio = models.FileField(upload_to='audio_messages/', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    recorded_together = models.BooleanField(default=False)
    def __str__(self):
        return self.message