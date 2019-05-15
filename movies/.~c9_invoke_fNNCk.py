import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from accounts.forms import UserCustomCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse, HttpResponseBadRequest

from rest_framework.decorators import api_view
from .serializers import ScoreSerializer, MovieSerializer
from rest_framework.response import Response

from .models import Movie, Genre, Hashtag, Score
from .forms import ScoreForm

# Create your views here.
# 영화 목록(맨처음 보여지는 곳)
# def list(request):
#     movies = Movie.objects.all()
#     context = {'movies':movies}
#     return render(request, 'movies/list.html', context)
    
@require_http_methods(['GET', 'POST'])
def list(request):
    # 해시태그별
    hashtags = Hashtag.objects.all()
    # 영화정보
    genres = []
    movies = []
    today = datetime.datetime.now()
    d = datetime.timedelta(days=90)
    before = today - d
    new_movies = Movie.objects.filter(open_date__range=[str(before.strftime("%Y-%m-%d")), str(today.strftime("%Y-%m-%d"))]).order_by('?')[:12]
    # print(new_movies)
    if request.user.is_authenticated:
        genres = request.user.like_genres.order_by('?')[:3]
        genre_movies = {}
        for genre in genres:
            # print(genre)
            # print(genre.movies.all().order_by('?')[:6])
            genre_movies[genre.name] = genre.movies.all().order_by('?')[:6]
        #     print(genre_movies[genre.name])
        # print(genre_movies)
        
        movies = Movie.objects.all()
        
    
    # 로그인form
    if request.method == "POST":
        user_form = AuthenticationForm(request, request.POST)
        if user_form.is_valid():
            user_form = auth_login(request, user_form.get_user())
            return redirect('movies:list')
    else:
        user_form = AuthenticationForm()
    # 회원가입 모달을 위한 회원가입 form
    userlists = get_user_model().objects.all()
    signup_form = UserCustomCreationForm()
    context = {'movies':movies, 'genres': genres, 'login_form':user_form, 'signup_form': signup_form, 
                'userlists':userlists, 'genre_movies': genre_movies, 'new_movies': new_movies, 
                'hashtags': hashtags
    }
    
    return render(request, 'movies/list.html', context)
    

def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    context = {'movie':movie}
    return render(request, 'movies/detail.html', context)
    return render(request, )
        
def detail_star(request, movie_pk):
    if request.is_ajax():
        p
        movie = get_object_or_404(Movie, pk=movie_pk)
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        return HttpResponseBadRequest
    
    
# 좋아하는 영화
def like_movie(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        # user가 지금 해당 게시글에 좋아요를 한 적이 있는지?
        print(movie.like_users)
        if movie.like_users.filter(pk=user.id).exists():
            movie.like_users.remove(user)

        else:
            movie.like_users.add(user)

        # return redirect('accounts:mypage', user_name)
        # return redirect(request.GET.get('next') or 'posts:list')
        return JsonResponse({})
    else:
        return HttpResponseBadRequest
    


@api_view(['POST'])
def createscore(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    serializer = ScoreSerializer(data=request.data)
    print(request.data)
    print(serializer)
    if request.user in movie.score_users.all():
        score = Score.objects.get(user=request.user)
        score.grade = request.data['grade']
        
    else:
        if serializer.is_valid(raise_exception=True):
            tmp = serializer.save(movie=movie, user=request.user)
            print("hi")
            print(tmp)
            return Response(MovieSerializer(movie).data)
            # if request.method == "POST":
            #     score_form = ScoreForm(request.POST)
            #     if score_form.is_valid():
            #         score = score_form.save(commit=False)
            #         score.movie = movie
            #         score.user = request.user
            #         score = score.save()
            #         return Response(serializer.data)
            # context = {'score_form':score_form}
            # return JsonResponse(context)
        else:
            return HttpResponseBadRequest
    

# 좋아하는 장르
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

