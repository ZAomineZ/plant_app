from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.text import slugify

from plant.forms import PlantForm
from plant.models import Plant, ImagePlant


def plants(request):
    return render(request, 'admin/plants/index.html')


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
            Plant.objects.create(title=title, slug=slug, description=description, category=category, image=image)
            # Redirect with success message
            messages.success(request, 'Vous avez crée une plante avec succès !')
            return HttpResponseRedirect(reverse('admin:plants'))
        else:
            errors = form.errors
            print(errors)
    else:
        form = PlantForm()
    return render(request, 'admin/plants/create.html', {'form': form, 'errors': errors})


def getImagePlant(image) -> ImagePlant:
    fs = FileSystemStorage()
    filename = fs.save(image.name, image)
    uploaded_file_url = fs.url(filename)
    # Create new image plant model
    ImagePlant.objects.create(title=image.name, image=uploaded_file_url)
    return ImagePlant.objects.filter(title=image.name).get()
