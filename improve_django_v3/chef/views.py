from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from .forms import ChefRegisterationForm, ChefAuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
from django.urls import reverse
# Create your views here.

def register_chef(request):
    if request.method == 'POST':
        new_user_form = ChefRegisterationForm(request.POST)
        if new_user_form.is_valid():
            user = new_user_form.save()
            login(request, user)
            messages.info(
                request,
                f"Logged in: {user}!"
            )
            return HttpResponseRedirect(reverse("menu:menu_list"))
    else:
        new_user_form = ChefRegisterationForm()
    return render(request, 'chef/register_chef.html', {'form': new_user_form})


def login_chef(request):
    if request.method == 'POST':
        login_form = ChefAuthenticationForm(data=request.POST)
        if login_form.is_valid():
            user = authenticate(**login_form.cleaned_data)
            if user:
                login(request, user)
                messages.info(request, f"Welcome {user}!")
                return HttpResponseRedirect(reverse("menu:menu_list"))
        messages.info(request, "Login failed. Please try again")
    login_form = ChefAuthenticationForm()
    return render(request, 'chef/login_chef.html', {'form': login_form})


@login_required
def logout_chef(request):
    logout(request)
    messages.info(request, "You are not logged out!")
    return HttpResponseRedirect(reverse("menu:menu_list"))
    

