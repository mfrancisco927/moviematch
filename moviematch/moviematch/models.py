from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseModel(models.Model):
    created_at = models.DateTimeField('created_time', auto_now_add=True, db_index=True, null=True)
    updated_at = models.DateTimeField('modified_time', auto_now=True)
    class Meta:
        abstract = True


class Profile(BaseModel):
    user = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    friends = models.ManyToManyField("self", related_name='profile_friends', symmetrical=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Media(BaseModel):
    imdbID = models.TextField(primary_key=True)
    title = models.TextField(max_length=500, blank=False)
    year = models.TextField(blank=False) #not int because shows have a range, ex Breaking Bad 2008-2013
    mpaa_rating = models.TextField(max_length=10, blank=False) #G, PG, PG-13, R, NC-17
    release_date = models.TextField()
    runtime = models.TextField()
    genres = models.ManyToManyField("Genre", related_name='media_genre', blank=True)
    director = models.TextField()
    writer = models.ManyToManyField("Writer", related_name='media_writer', blank=True)
    actors = models.ManyToManyField("Actor", related_name='media_actor', blank=True)
    plot = models.TextField(max_length=500, blank=False)
    country = models.TextField(max_length=20, blank=False)
    poster_link = models.TextField(max_length=500, blank=False)
    imdb_rating = models.FloatField()
    medium = models.TextField(max_length=20, blank=False)


class Actor(BaseModel):
    name = models.TextField()

class Genre(BaseModel):
    name = models.TextField()

class Writer(BaseModel):
    name = models.TextField()

