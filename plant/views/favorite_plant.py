from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from plant.models import FavoritePlant, Plant


@login_required
def index(request, username: str):
    user = get_object_or_404(User, username=username)
    if request.user.username != user.username:
        return HttpResponseRedirect(reverse('plant:index'))

    plants_favorite = FavoritePlant.objects.filter(user=user).all()
    return render(request, 'plant/favorite_plant/index.html', {'plants_favorite': plants_favorite})


@login_required
def add(request, username: str, plant_slug: str):
    user = get_object_or_404(User, username=username)
    plant = get_object_or_404(Plant, slug=plant_slug)
    if request.user.username != user.username:
        return HttpResponseRedirect(reverse('plant:index'))

    # Add the plant current in the favorite plant model to user authenticated
    if not FavoritePlant.objects.filter(user=user, plant=plant):
        FavoritePlant.objects.create(user=user, plant=plant)
    else:
        messages.error(request, 'Vous avez déjà ajouté cette plante dans vos favoris !')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def delete(request, username: str, plant_slug: str):
    user = get_object_or_404(User, username=username)
    plant = get_object_or_404(Plant, slug=plant_slug)
    if request.user.username != user.username:
        return HttpResponseRedirect(reverse('plant:index'))

    # Delete the plant current in the favorite plant model to user authenticated
    favorite_plant = FavoritePlant.objects.filter(user=user, plant=plant)
    if favorite_plant.exists():
        favorite_plant.delete()
    else:
        messages.error(request, 'Vous ne pouvez pas supprimier une plante qui n\'est pas dans vos favoris !')