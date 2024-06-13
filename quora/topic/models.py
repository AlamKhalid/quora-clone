from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    picture = models.ImageField(upload_to='topics')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name='following')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    
class Question(models.Model):
    description = models.TextField()
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='qs_liked_by')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    disliked_by = models.ManyToManyField(User, related_name='qs_disliked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description
    
    
class Answer(models.Model):
    description = models.TextField()
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='ans_liked_by')
    disliked_by = models.ManyToManyField(User, related_name='ans_disliked_by')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.description