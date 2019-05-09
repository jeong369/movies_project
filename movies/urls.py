from django.urls import path
from . import views

app_name = "movies"

urlpatterns = [
        path('', views.list, name="list"),
        path('<int:movie_pk>/', views.detail, name="detail"),
        path('<int:movie_pk>/createscore/', views.createscore, name="createscore"),
]