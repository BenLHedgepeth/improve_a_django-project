from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from .forms import ChefRegisterationForm
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password
# Create your views here.

def register_chef(request):
    if request.method == 'POST':
        new_user_form = ChefRegisterationForm(request.POST)
        if new_user_form.is_valid():
            try:
                user = User.objects.get(
                    username=new_user_form.cleaned_data['username']
                )
                stored_password = check_password(
                    new_user_form.cleaned_data['check_password'], 
                    user.password
                )
            except User.DoesNotExist:
                user = new_user_form.save()
                login(request, user)
                messages.info(f"Logged in: {user}")
                return HttpResponseRedirect(reverse("menu:menu_list"))
            else:
                if stored_password:
                    messages.info(
                        request,
                        "You already registered an account. Please log in."
                    )
                else:
                    messages.info(
                        request, 
                        f"Username {username} exists. Choose another username."
                    )
                return HttpResponseRedirect(reverse("chef:create_chef"))
        messages.info(
            request, 
            "Registeration failed. Please try again."
        )
    new_user_form = ChefRegisterationForm()
    return render(request, "chef/register_chef.html", {'form': new_user_form})


def login_chef(request):
    pass