from django.db import models
from django.contrib.auth.models import User
  
class Gender(models.TextChoices):
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class Profile(models.Model):
    user = models.OneToOneField(
        User, related_name='profile', on_delete=models.CASCADE)
    image = models.ImageField(
        upload_to="profile_picture", default="default.jpeg", null=True)
    age = models.PositiveIntegerField()
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.OTHER,
    )
    
    
    def __str__(self):
        return f'{self.username} {self.email}'


