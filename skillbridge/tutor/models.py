from django.db import models

class Mentor(models.Model):
    name = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255, default="None")
    skill_level = models.IntegerField()
    available_time = models.CharField(max_length=255, default="Not Available")
    teaching_mode = models.CharField(max_length=255, default="virtual")
    rating = models.FloatField()
    email = models.EmailField()
    
    # Temporary fields for displaying rank and predicted score
    predicted_score = models.FloatField(null=True, blank=True)
    rank = models.FloatField(null=True, blank=True)

    def __str__(self):  
        return self.name



class Request(models.Model):
    mentee_name = models.CharField(max_length=100)
    mentee_email = models.EmailField()
    mentor = models.ForeignKey(Mentor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, default='Pending')  # 'Pending', 'Accepted', 'Rejected'
