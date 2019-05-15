from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    # def __str__(self):
    #     return f'{self.pk} : {self.name}'
    
class Actor(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    
class Hashtag(models.Model):
    content = models.TextField(blank=True)

class Movie(models.Model):
    title = models.CharField(max_length=150)
    en_title = models.CharField(max_length=150, blank=True)
    genres = models.ManyToManyField(Genre, related_name="movies", blank=True)
    open_date = models.DateField(blank=True)
    director = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor, related_name="movies", blank=True)
    rated = models.CharField(max_length=150, blank=True)
    summary = models.TextField(blank=True)
    imageurl = models.CharField(max_length=150, blank=True)
    hashtags = models.ManyToManyField(Hashtag, blank=True, related_name="movies")
    score_users = models.ManyToManyField(settings.AUTH_USER_MODEL, through='Score', related_name='score_movies')

class Score(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    grade = models.IntegerField()
    