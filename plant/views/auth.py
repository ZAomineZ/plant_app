from django.contrib import messages
from django.contrib.auth import authenticate, login as login_action
from django.contrib.auth import logout as logout_action
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from plant.decorators import logout_required
from plant.forms import RegisterForm, LoginForm
from plant.models import CustomUser


@logout_required
def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            email = form.clean_email()
            password = form.cleaned_data['password']
            CustomUser.objects.create(username=username, email=email, password=make_password(password))
            # Add message success
            messages.success(request, 'Vous avez créé votre compte')
            return HttpResponseRedirect(reverse('plant:auth.login'))
        else:
            messages.error(request, 'Le formulaire n\'est pas valide')
    return render(request, 'plant/auth/register.html', {'form': form})


@logout_required
def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.clean_username()
            password = form.cleaned_data['password']

            userCurrent = CustomUser.objects.filter(username=username).first()
            user: CustomUser | None = authenticate(request, username=userCurrent.username, password=password)
            if user and not None and user.is_active:
                login_action(request, user)
                # Add message success
                messages.success(request, 'Vous êtes maitenant connecté')
                return HttpResponseRedirect(reverse('plant:index'))
        else:
            messages.error(request, 'Le formulaire n\'est pas valide')
    return render(request, 'plant/auth/login.html', {'form': form})


@login_required
def logout(request):
    logout_action(request)
    messages.success(request, 'Vous êtes maitenant déconnecté')
    return HttpResponseRedirect(reverse('plant:index'))
