from django.db import models
from django.contrib.auth.models import User

# User profile model, as you've already defined


class UserProfile(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    skill_name = models.CharField(max_length=100)
    skill_level = models.CharField(
        max_length=20,
        choices=[
            ('intermediate', 'Intermediate'),
            ('advanced', 'Advanced'),
            ('professional', 'Professional'),
        ]
    )
    time_available = models.CharField(max_length=50)
    email = models.EmailField(max_length=255, unique=True)  # Added email field

    def __str__(self):
        return self.username


from django.db import models
from django.contrib.auth.models import User

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} at {self.timestamp}"
