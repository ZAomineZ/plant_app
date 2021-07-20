from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify

from plant.forms import PlantForm, CategoryForm
# Create your views here.
from plant.models import Category


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


def categories(request):
    categories = Category.objects.all()
    return render(request, 'admin/categories/index.html', {'categories': categories})


def categories_create(request):
    errors = None

    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            # Save new category
            slug = slugify(title)
            Category.objects.create(title=title, slug=slug, description=description)

            messages.success(request, 'Tu as crée ta catégorie avec success !')
            return HttpResponseRedirect(reverse('admin:categories'))
        else:
            errors = form.errors
    else:
        form = PlantForm()
    return render(request, 'admin/categories/create.html', {'form': form, 'errors': errors})
