from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCustomCreationForm
from .models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST
from django.http import JsonResponse, HttpResponseBadRequest

from rest_framework.decorators import api_view
from movies.serializers import MovieSerializer, UserSerializer, ScoreSerializer
from rest_framework.response import Response

from movies.models import Movie, Genre, Score, Hashtag


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
    hashtags = Hashtag.objects.all()
    genrelists = Genre.objects.all()
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == "POST":
        user_form = AuthenticationForm(request, request.POST)
        if user_form.is_valid():
            user_form = auth_login(request, user_form.get_user())
            return redirect('movies:list')
    else:
        user_form = AuthenticationForm()
    context = {'user_form':user_form, 'hashtags': hashtags, 'genrelists':genrelists,}
    return render(request, 'accounts/form.html', context)
    
@login_required
def logout(request):
    user_form = auth_logout(request)
    return redirect('movies:list')
    
@login_required
def userdelete(request):
    request.user.delete()
    return redirect('movies:list')
    
@login_required
def info(request, user_pk):
    User = get_user_model()
    user = User.objects.get(pk=user_pk)
    leng_genre = len(user.like_genres.all())
    leng_movie = len(user.like_movies.all())
    hashtags = Hashtag.objects.all()
    genrelists = Genre.objects.all()
    context = {'user':user, 'leng_genre':leng_genre, 'leng_movie':leng_movie, 'hashtags': hashtags, 'genrelists':genrelists,}
    return render(request, 'accounts/info.html', context)

# 평가 페이지
@login_required
def evaluate(request):
    # 해시태그별
    hashtags = Hashtag.objects.all()
    # all genre
    genrelists = Genre.objects.all()
    genres = Genre.objects.all()
    movies = Movie.objects.order_by('?')[:30]
    userlists = get_user_model().objects.all()
    context = {'movies': movies, 'genres': genres, 'userlists':userlists,
                'genrelists':genrelists, 'hashtags':hashtags,
    }
    # print(movies)
    return render(request, 'accounts/evaluate.html', context)



# Create your views here.

# @api_view(['GET'])
# def music_list(request):
#     '''음악 정보 출력'''
#     musics = Music.objects.all()
#     serializer = MusicSerializer(musics, many=True)
#     return Response(serializer.data)
    

# 평점 영화 목록
@api_view(['POST'])
@login_required
def evaluate_movies(request):
    # 영화정보
    if request.is_ajax():
        start_movie = request.user.score_set.all()
        my_results = Movie.objects.all()
        for tmpmovie in start_movie:
            my_results = my_results.exclude(id=tmpmovie.movie.id)
        print("my_result", my_results.count())
        print('start_movie', start_movie.count())
        movies = my_results.order_by('?')[:30]
        for movie in movies:
            if request.user in movie.like_users.all():
               movie.is_like = True
            else:
                movie.is_like = False
            print(movie.is_like)
        serializer = MovieSerializer(movies, many=True)
        data = serializer.data
        data.insert(0, [{'like_count': start_movie.count()}])
        # print(data)
        return Response(data)
    else:
        return HttpResponseBadRequest

    

@api_view(['POST'])
def follow(request, user_pk):
    User = get_user_model()
    if request.is_ajax():
        follow_user = get_object_or_404(User, pk=user_pk)
        if request.user not in follow_user.followers.all() :
            follow_user.followers.add(request.user)
            is_follow = False
        else:
            follow_user.followers.remove(request.user)
            is_follow = True
        return JsonResponse({'is_follow':is_follow})
    else:
        return HttpResponseBadRequest
        
    
    
@api_view(['GET', 'POST'])
def findfollow(request):
    User = get_user_model()
    mainuser = request.user
    users = User.objects.all().exclude(pk=mainuser.pk)
    someusers = users.order_by('?')[:5]
    # allscore = []
    for anyuser in someusers :
        # print(anyuser)
        if anyuser in request.user.followings.all():
            anyuser.is_follow = True
        else:
            anyuser.is_follow = False
        movies = []
        for score in anyuser.score_set.all().order_by('-grade')[:5]:
            tmp_movie = Movie.objects.get(pk=score.movie.pk)
            movies.append(tmp_movie)
        # allscore.append(scores)
        anyuser.recommend_movies = movies
        
    context = {'someusers': someusers}
    if request.is_ajax():
        serializer = UserSerializer(someusers, many=True)
        if request.method == "POST":
            return Response(serializer.data)
        else:
            return HttpResponseBadRequest
    else:
        return render(request, 'accounts/findfollow.html', context)