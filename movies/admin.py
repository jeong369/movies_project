from django.contrib import admin
from .models import Movie, Genre, Actor, Score, Hashtag
# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Actor)
admin.site.register(Score)
admin.site.register(Hashtag)