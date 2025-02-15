import os

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
            # Other fields for the filter
            shade = form.cleaned_data['shade']
            moisture = form.cleaned_data['moisture']
            wind = form.cleaned_data['wind']
            soil = form.cleaned_data['soil']
            growth_rate = form.cleaned_data['growth_rate']

            image = getImagePlant(form.cleaned_data['image'])
            # Save plant model
            Plant.objects.create(title=title, slug=slug, description=description, category=category, image=image,
                                 shade=shade, moisture=moisture, wind=wind, soil=soil, growth_rate=growth_rate)
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
            # Other fields for the filter
            shade = form.cleaned_data['shade']
            moisture = form.cleaned_data['moisture']
            wind = form.cleaned_data['wind']
            soil = form.cleaned_data['soil']
            growth_rate = form.cleaned_data['growth_rate']

            if form.cleaned_data['image'] is not None:
                image = getImagePlant(form.cleaned_data['image'])
            else:
                image = plant.image
            # Save plant model
            plant.title = title
            plant.slug = slug
            plant.description = description
            plant.category = category
            plant.shade = shade
            plant.moisture = moisture
            plant.wind = wind
            plant.soil = soil
            plant.growth_rate = growth_rate
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


def plant_delete(request, plant_id: int):
    plant = Plant.objects.filter(pk=plant_id)
    if not plant.exists():
        messages.error(request, 'Vous ne pouvez pas supprimer une plant qui n\'éxiste pas')
    else:
        plant_model = plant.first()
        if os.path.isfile(plant_model.image.image.path):
            os.remove(plant_model.image.image.path)
            plant_model.image.delete()
        plant.delete()
        messages.error(request, 'Vous avez supprimé cette plant avec success')
    return HttpResponseRedirect(reverse('admin:plants'))


def getImagePlant(image) -> ImagePlant:
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    # Create new image plant model
    return ImagePlant.objects.create(title=image.name, image=filename)
