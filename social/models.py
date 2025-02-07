from django.db import models
from datetime import datetime
from django.contrib.auth import get_user_model

User = get_user_model()


class Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True, default=0)


    def __str__(self):
        return self.user.username