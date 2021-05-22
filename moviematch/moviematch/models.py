from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseModel(models.Model):
  created_at = models.DateTimeField('created_time', auto_now_add=True, db_index=True, null=True)
  updated_at = models.DateTimeField('modified_time', auto_now=True)

class Profile(BaseModel):
  user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
  friends = models.ManyToManyField("self", related_name='profile_friends', symmetrical=True, blank=True)
  bio = models.TextField(max_length=500, blank=True)
  refresh_token = models.TextField(default="None")
  '''
  liked_songs = models.ManyToManyField(Song, related_name='profile_liked', blank=True)
  disliked_songs = models.ManyToManyField(Song, related_name='profile_disliked', blank=True)
  favorite_playlists = models.ManyToManyField("Playlist", related_name='profile_favorite_playlists', blank=True)
 
  image = models.ImageField(blank=True, null=True)
  '''
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()