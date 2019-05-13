from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCustomCreationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST

from movies.models import Movie, Genre


# Create your views here.

@require_http_methods(['POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    user_form = UserCustomCreationForm(request.POST)
    if user_form.is_valid():
        user = user_form.save()
        auth_login(request, user)
        return redirect("accounts:evaluate")

    
@require_http_methods(['GET', 'POST'])
def login(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == "POST":
        user_form = AuthenticationForm(request, request.POST)
        if user_form.is_valid():
            user_form = auth_login(request, user_form.get_user())
            return redirect('movies:list')
    else:
        user_form = AuthenticationForm()
    context = {'user_form':user_form}
    return render(request, 'accounts/form.html', context)
    
@login_required
def logout(request):
    user_form = auth_logout(request)
    return redirect('movies:list')
    
@login_required
def info(request, user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    leng_genre = len(user.like_genres.all())
    leng_movie = len(user.like_movies.all())
    context = {'user':user, 'leng_genre':leng_genre, 'leng_movie':leng_movie}
    return render(request, 'accounts/info.html', context)

@login_required
def evaluate(request):
    genres = Genre.objects.all()
    movies = Movie.objects.order_by('?')[:30]
    userlists = get_user_model().objects.all()
    context = {'movies':movies, 'genres': genres, 'userlists':userlists}
    print(movies)
    return render(request, 'accounts/evaluate.html', context)
    
@login_required
def follow(request, user_pk):
    User = get_user_model()
    follow_user = User.objects.get(pk=user_pk)
    if request.user not in follow_user.followers.all() :
        follow_user.followers.add(request.user)
    else:
        follow_user.followers.remove(request.user)
    return redirect('movies:list')
    