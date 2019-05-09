from django.shortcuts import render, redirect
from .models import Movie
from .forms import ScoreForm

# Create your views here.
# 영화 목록(맨처음 보여지는 곳)
def list(request):
    movies = Movie.objects.all()
    context = {'movies':movies}
    return render(request, 'movies/list.html', context)
    

def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    context = {'movie': movie}
    return render(request, 'movies/detail.html', context)
    
    
# 평점주기
def createscore(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    if request.method == "POST":
        score_form = ScoreForm(request.POST)
        if score_form.is_valid():
            score = score_form.save(commit=False)
            score.movie = movie
            score.user = request.user
            score = score.save()
            return redirect('movies:list')
    else:
        score_form = ScoreForm()
    context = {'score_form':score_form}
    return render(request, 'movies/createscore.html', context)