from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render


# Create your views here.
from plant.forms import PlantForm


def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(email=email, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/superadmin')

    return render(request, 'admin/index.html')


def plants(request):
    return render(request, 'admin/plants/index.html')


def plant_create(request):
    if request.method == 'POST':
        print('Tu fais quelque chose')
    else:
        form = PlantForm()
    return render(request, 'admin/plants/create.html', {'form': form})
