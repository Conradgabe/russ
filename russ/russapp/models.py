from django.db import models

# Create your models here.
class LoginCredentials(models.Model):
    username = models.CharField(max_length=20)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.username
    
    class Meta:
        ordering = ['username']