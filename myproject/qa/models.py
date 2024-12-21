# qa/models.py
from django.db import models
from django.contrib.auth.models import User  # For associating questions and replies with users

# Model to store questions
class Question(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who asked the question
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Model to store replies to questions
class Reply(models.Model):
    question = models.ForeignKey(Question, related_name='replies', on_delete=models.CASCADE)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # The user who replied
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply to: {self.question.title}"
