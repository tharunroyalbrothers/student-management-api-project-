from django.db import models

class Student(models.Model):
    usn = models.CharField(max_length=10, unique=True)  
    name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    course = models.CharField(max_length=45)
    age  = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.name} ({self.usn})"
