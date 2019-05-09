from django.shortcuts import render
from django.contrib.auth import login as auth_login

# Create your views here.
def signup(request):
    return render(request, 'accounts/signup.html')