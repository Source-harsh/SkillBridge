from django.db import models
from django.contrib.auth.models import User

# User profile model, as you've already defined



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    skill_name = models.CharField(max_length=100)
    professionalism_level = models.CharField(
        max_length=20,
        choices=[('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Professional', 'Professional')],
    )

    def __str__(self):
        return self.user.username



# Collaboration request model
# models.py in 'home' app



class CollaborationRequest(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_requests')
    skill_needed = models.CharField(max_length=100)
    professionalism_level_needed = models.CharField(
        max_length=20,
        choices=[('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Professional', 'Professional')],
        default='Intermediate'
    )
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Accepted', 'Accepted'), ('Declined', 'Declined')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request from {self.from_user.username} to {self.to_user.username} for skill {self.skill_needed} with professionalism level {self.professionalism_level_needed}"
