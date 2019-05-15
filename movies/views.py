import datetime
import pprint

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

from Collaborative_Filtering.filtering import getRecommendation, top_match


# Create your views here.
# 영화 목록(맨처음 보여지는 곳)
# def list(request):
#     movies = Movie.objects.all()
#     context = {'movies':movies}
#     return render(request, 'movies/list.html', context)
    
@require_http_methods(['GET', 'POST'])
def list(request):
    # 해시태그별
    hashtags = Hashtag.objects.all().prefetch_related('movies')
    # all genre
    genrelists = Genre.objects.all()
    # 영화정보
    genres = []
    movies = []
    today = datetime.datetime.now()
    d = datetime.timedelta(days=90)
    before = today - d
    new_movies = Movie.objects.filter(open_date__range=[str(before.strftime("%Y-%m-%d")), str(today.strftime("%Y-%m-%d"))]).order_by('?')[:12]
    # print(new_movies)
    genre_movies = {}
    if request.user.is_authenticated:
        genres = request.user.like_genres.prefetch_related('movies').order_by('?')[:3]
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
                'hashtags': hashtags, 'genrelists':genrelists,
    }
    
    return render(request, 'movies/list.html', context)
    
# 장르 디테일 페이지
def genre_detail(request, genre_pk):
    genre = get_object_or_404(Genre, pk=genre_pk)
    context = {'genre':genre}
    return render(request, 'movies/genre_detail.html', context)


# 영화 디테일 페이지
def detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
        # 해시태그별
    hashtags = Hashtag.objects.all()
    # all genre
    genrelists = Genre.objects.all()
    context = {'movie':movie, 'hashtags': hashtags, 'genrelists':genrelists,}
    return render(request, 'movies/detail.html', context)
        

@api_view(['POST'])
def detail_star(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        score = Score.objects.filter(movie=movie, user=request.user)
        if score:
            # print(score)
            score = score[0].grade
        else:
            score = 0
        # print(score)
        serializer = MovieSerializer(movie)
        movie_data = serializer.data
        # print(movie_data)
        movie_data.update({'score': score})
        # print(movie_data)
        # print(serializer.data)
        return Response(movie_data)
    else:
        return HttpResponseBadRequest
    
    
# 좋아하는 영화
def like_movie(request, movie_pk):
    if request.is_ajax():
        movie = get_object_or_404(Movie, pk=movie_pk)
        user = request.user
        # user가 지금 해당 게시글에 좋아요를 한 적이 있는지?
        # print(movie.like_users)
        if movie.like_users.filter(pk=user.id).exists():
            movie.like_users.remove(user)
        else:
            movie.like_users.add(user)

        # return redirect('accounts:mypage', user_name)
        # return redirect(request.GET.get('next') or 'posts:list')
        return JsonResponse({})
    else:
        return HttpResponseBadRequest


#  J      B
# GOT TA KI (GTK)
     
 

# 별점 생성
@api_view(['POST'])
def createscore(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    current_movie = MovieSerializer(movie).data
    # print(current_movie)
    serializer = ScoreSerializer(data=request.data)
    # print(request.data)
    # print(serializer)
    if request.user in movie.score_users.all():
        # print("dsaghowijfoaiaifiowaeifej")
        # print(request)
        score = Score.objects.filter(user=request.user, movie=movie)[0]
        # print(request.data)
        score.grade = request.data['grade']
        # print(score)
        score.save()
        current_movie.update({'is_update': True})
        return Response(current_movie)
    else:
        if serializer.is_valid(raise_exception=True):
            tmp = serializer.save(movie=movie, user=request.user)
            # print("hi")
            # print(tmp)
            current_movie.update({'is_update': False})
            return Response(current_movie)
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



'''

def evaluate_movies(request):
    if request.is_ajax():
        start_movie = request.user.score_set.all()
        my_results = Movie.objects.all()
        for tmpmovie in start_movie:
            my_results = my_results.exclude(id=tmpmovie.movie.id)
        print("my_result", my_results.count())
        print('start_movie', start_movie.count())
        movies = my_results.order_by('?')[:30]
        serializer = MovieSerializer(movies, many=True)
        data = serializer.data
        data.insert(0, [{'like_count': start_movie.count()}])
        # print(data)
        return Response(data)
    else:
        return HttpResponseBadRequest
'''


@api_view(['POST'])
@login_required
def recommend_movies(request):
    if request.is_ajax():
        scores = Score.objects.all()
        critics = {}
        for score in scores:
            check = critics.get(score.user_id, None)
            if not check:
                critics[score.user_id] = {score.movie_id: score.grade}
            else:
                critics[score.user_id].update({score.movie_id: score.grade})
            
        recommend_list = getRecommendation(critics, request.user.pk)
        movies = []
        for i in range(10):
            recommendation = recommend_list[i]
            current_movie = Movie.objects.get(pk=recommendation[1])
            # print("%0.1f" % recommendation[0])
            current_movie.expected_score = float("%0.1f" % recommendation[0])
            # print(current_movie.expected_score)
            movies.append(current_movie)
        data = []
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    else:
        return HttpResponseBadRequest