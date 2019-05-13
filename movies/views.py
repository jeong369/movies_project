from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import UserCustomCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse, HttpResponseBadRequest

from .models import Movie, Genre
from .forms import ScoreForm

# Create your views here.
# 영화 목록(맨처음 보여지는 곳)
# def list(request):
#     movies = Movie.objects.all()
#     context = {'movies':movies}
#     return render(request, 'movies/list.html', context)
    
@require_http_methods(['GET', 'POST'])
def list(request):
    if request.user.is_authenticated:
        movies = Movie.objects.all()
    else:
        movies = []
    
    if request.method == "POST":
        user_form = AuthenticationForm(request, request.POST)
        if user_form.is_valid():
            user_form = auth_login(request, user_form.get_user())
            return redirect('movies:list')
    else:
        user_form = AuthenticationForm()
    userlists = get_user_model().objects.all()
    print(userlists)
    signup_form = UserCustomCreationForm()
    context = {'movies':movies, 'login_form':user_form, 'signup_form': signup_form, 'userlists':userlists}
    
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

@login_required
def like_genres(request, genre_pk):
    if request.is_ajax():
        genre = get_object_or_404(Genre, pk=genre_pk)
        user = request.user
        # user가 지금 해당 게시글에 좋아요를 한 적이 있는지?
        
        if genre.like_users.filter(pk=user.id).exists():
            genre.like_users.remove(user)
            is_like = False
        else:
            genre.like_users.add(user)
            is_like = True
        # return redirect('accounts:mypage', user_name)
        # return redirect(request.GET.get('next') or 'posts:list')
        return JsonResponse({'is_like': is_like})
    else:
        return HttpResponseBadRequest

