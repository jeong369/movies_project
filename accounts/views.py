from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserCustomCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_POST

# Create your views here.

@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('movies:list')
    if request.method == "POST":
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
            return redirect("movies:list")
    else:
        user_form = UserCustomCreationForm()
    context = {'user_form':user_form}
    return render(request, 'accounts/form.html', context)
    
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