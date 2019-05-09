from django.shortcuts import render
from django.contrib.auth import login as auth_login
from .forms import UserCustomCreationForm

# Create your views here.
def signup(request):
    if request.method == "POST":
        user_form = UserCustomCreationForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            auth_login(request, user)
    else:
        user_form = UserCustomCreationForm()
    context = {'user_form':user_form}
    return render(request, 'accounts/signup.html', context)