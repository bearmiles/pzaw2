from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True, default=0)
    profileimg = models.ImageField(upload_to='social/prof/', default='social/prof/dc1.png')

    def __str__(self):
        return self.user.username
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profileimg = models.ImageField(upload_to="profile_pics/", default="social/prof/dc1.png")
    club = models.CharField(max_length=100, default="Unknown")
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

