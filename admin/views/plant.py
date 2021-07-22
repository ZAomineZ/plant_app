from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.text import slugify

from plant.forms import PlantForm
from plant.models import Plant, ImagePlant


def plants(request):
    plants = Plant.objects.all()
    return render(request, 'admin/plants/index.html', {'plants': plants})


def plant_create(request):
    errors = None

    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        # Check the form is valid
        if form.is_valid():
            title = form.cleaned_data['title']
            slug = slugify(title)
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            image = getImagePlant(form.cleaned_data['image'])
            # Save plant model
            Plant.objects.create(title=title, slug=slug, description=description, category=category, image=image)
            # Redirect with success message
            messages.success(request, 'Vous avez crée une plante avec succès !')
            return HttpResponseRedirect(reverse('admin:plants'))
        else:
            errors = form.errors
    else:
        form = PlantForm()
    return render(request, 'admin/plants/create.html', {'form': form, 'errors': errors})


def plant_edit(request, plant_id: int):
    plant = get_object_or_404(Plant, pk=plant_id)
    errors = None
    if request.method == 'POST':
        form = PlantForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            slug = slugify(title)
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            if form.cleaned_data['image'] is not None:
                image = getImagePlant(form.cleaned_data['image'])
            else:
                image = plant.image
            # Save plant model
            plant.title = title
            plant.slug = slug
            plant.description = description
            plant.category = category
            plant.image = image
            plant.save()
            # Redirect with success message
            messages.success(request, 'Vous avez edité une plante avec succès !')
            return HttpResponseRedirect(reverse('admin:plants'))
        else:
            errors = form.errors
    else:
        form = PlantForm(instance=plant)

    return render(request, 'admin/plants/edit.html', {'form': form, 'errors': errors})


def getImagePlant(image) -> ImagePlant:
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    uploaded_file_url = 'plant' + fs.url(filename)
    # Create new image plant model
    return ImagePlant.objects.create(title=image.name, image=uploaded_file_url)
