from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.

class Live_User(models.Model):
    class Meta:
        verbose_name = "Live_User"
        verbose_name_plural = "Live_Users"
        ordering = ["user_id"]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uniq_userid = models.CharField(max_length=20, blank=True)
    profile_pic = models.ImageField(verbose_name="Profile Pic", upload_to='profile_pics')

    def __str__(self):
        return f'User-ID: {self.uniq_userid}'

class Room(models.Model):
    class Meta:
        verbose_name = "Room"
        verbose_name_plural = "Rooms"
        ordering = ["room_id"]

    name = models.CharField(max_length=600)
    room_id = models.CharField(max_length=20, unique=True, blank=True)
    thumbnail = models.ImageField(verbose_name="Group Dp",upload_to='room_pics')

    def __str__(self):
        return f'Room-ID: {self.room_id}, Group-Name: {self.name}'

class Messages(models.Model):
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ["-date"]

    value = models.CharField(max_length=200000)
    date = models.DateTimeField(default=datetime.now(), blank=True)
    lu_ref = models.ForeignKey(Live_User, on_delete=models.CASCADE)
    room_ref = models.ForeignKey(Room, on_delete=models.CASCADE)


class Subscriptions(models.Model):
    class Meta:
        verbose_name = "Subscription"
        verbose_name_plural = "Subscriptions"
        ordering = ["room_ref", "lu_ref"]

    lu_ref = models.ForeignKey(Live_User, on_delete=models.CASCADE)
    room_ref = models.ForeignKey(Room, on_delete=models.CASCADE)
    last_visited = models.DateTimeField(default=datetime.now)

