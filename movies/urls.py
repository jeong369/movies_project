from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
        path('', views.list, name="list"),
        path('<int:movie_pk>/', views.detail, name="detail"),
        path('<int:movie_pk>/createscore/', views.createscore, name="createscore"),
        path('like_genres/<int:genre_pk>/', views.like_genres, name="like_genres"),
]