from django.db import models
from accounts.models import Profile

# Create your models here.
class Message(models.Model):
    body = models.CharField(max_length=255)
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='receiver')

    def __str__(self):
        return f"{self.sender}: {self.receiver}"
