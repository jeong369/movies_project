from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
        path('', views.list, name="list"),
        path('<int:movie_pk>/', views.detail, name="detail"),
        path('<int:movie_pk>/detail_star/', views.detail_star, name="detail_star"),
        path('<int:movie_pk>/createscore/', views.createscore, name="createscore"),
        path('like_genres/<int:genre_pk>/', views.like_genres, name="like_genres"),
        path('<int:movie_pk>/like/', views.like_movie, name="like_movie"),
        path('recommend_movies/', views.recommend_movies, name="recommend_movies"),
        path('genres/<int:genre_pk>/', views.genre_detail, name="genre_detail"),
        path('search/', views.search, name='search'),

]