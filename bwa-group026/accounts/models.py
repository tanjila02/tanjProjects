from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime

# Create your models here.

class CustomUser(AbstractUser):
    # add additional fields in here

    name = models.CharField(max_length=30, blank=True)
    username = models.CharField(max_length=30, blank=True, null=True, unique=True)

    email = models.EmailField( blank=True, null=True)
    phone_number = models.IntegerField(blank=True, null=True)
    address = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username

class FriendshipRequest(models.Model):
    from_user = models.ForeignKey(CustomUser, models.CASCADE, related_name='%(class)s_from_created')
    to_user = models.ForeignKey(CustomUser, models.CASCADE, related_name='%(class)s_to_created')
    class Meta:
        unique_together = ["from_user", "to_user"]

class Friend(models.Model):
    to_user = models.ForeignKey(CustomUser, models.CASCADE, related_name='%(class)s_from_created')
    from_user = models.ForeignKey(CustomUser, models.CASCADE, related_name='%(class)s_to_created')

    class Meta:
        unique_together = ["from_user", "to_user"]



class Chat(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser, models.CASCADE)

    def __str__(self):
        return self.message
