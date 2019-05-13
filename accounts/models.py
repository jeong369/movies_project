from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

from movies.models import Movie, Genre

# Create your models here.
class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="followings")
    like_genres = models.ManyToManyField(Genre, blank=True, related_name='like_users')
    like_movies = models.ManyToManyField(Movie, blank=True, related_name="like_users")

    
