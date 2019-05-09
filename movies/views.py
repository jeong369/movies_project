from django.shortcuts import render
from .models import Movie

# Create your views here.
def list(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/list.html', context)