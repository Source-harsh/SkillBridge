from django.db import models

class SubjectFile(models.Model):
    subject = models.CharField(max_length=100)
    file = models.FileField(upload_to='uploads/')

    def __str__(self):
        return self.subject