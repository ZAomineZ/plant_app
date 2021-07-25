from django.shortcuts import render


def index(request, username: str):
    return render(request, 'plant/favorite_plant/index.html')
