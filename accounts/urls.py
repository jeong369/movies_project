from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
        path('signup/', views.signup, name="signup"),
        path('login/', views.login, name="login"),
        path('logout/', views.logout, name="logout"),
        path('userdelete/', views.userdelete, name="userdelete"),
        path('evaluate/', views.evaluate, name='evaluate'),
        path('evaluate_movies/', views.evaluate_movies, name='evaluate_movies'),
        path('<int:user_pk>/', views.info, name="info"),
        path('<int:user_pk>/follow/', views.follow, name="follow"),
        path('findfollow/', views.findfollow, name="findfollow"),
]