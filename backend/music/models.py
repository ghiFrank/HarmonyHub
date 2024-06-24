from django.db import models
from django.contrib.auth.models import User

class Song(models.Model):
    spotify_id = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    genre = models.CharField(max_length=200, blank=True)
    album = models.CharField(max_length=200)
    release_date = models.DateField()
    duration_ms = models.IntegerField()
    popularity = models.IntegerField()

class UserInteraction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    interaction_type = models.CharField(max_length=50)  # e.g., 'played', 'liked'
    timestamp = models.DateTimeField(auto_now_add=True)
