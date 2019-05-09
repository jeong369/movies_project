from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
class Actor(models.Model):
    name = models.CharField(max_length=150)
    
    def __str__(self):
        return self.name
    

class Movie(models.Model):
    title = models.CharField(max_length=150)
    en_title = models.CharField(max_length=150)
    genres = models.ManyToManyField(Genre, related_name="movies")
    open_date = models.DateField()
    director = models.CharField(max_length=100)
    actors = models.ManyToManyField(Actor, related_name="movies")
    rated = models.CharField(max_length=150)
    summary = models.TextField()
    imageurl = models.CharField(max_length=150)


class Score(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    grade = models.IntegerField()
    