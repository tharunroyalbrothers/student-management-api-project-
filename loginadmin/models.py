from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=10,unique=True)

    def __str__(self):
        return self.user.username
    
    class Meta:
        managed = True
        db_table = "user_profiles"       
