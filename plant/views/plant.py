from django.contrib import messages
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from plant.forms import PlantFilterForm
from plant.models import Category, Plant
from plant.views.utils import Paginate


def index(request):
    pagePlant = None

    # Request
    params = list(request.GET.items())
    if request.method == 'GET' and len(params) != 0 and request.GET.get('reset_filter') is None:
        form = PlantFilterForm(request.GET)

        # Check exist category model in our BDD
        searchCategoryField = request.GET.get('search_category')
        if searchCategoryField is not None and len(searchCategoryField) != 0:
            category = Category.objects.filter(id=searchCategoryField).first()
            if category is None:
                messages.success(request, 'Cette catégorie n\'est pas présente dans notre base de donnée !')
                return HttpResponseRedirect(reverse('plant:index'))

        if form.is_valid():
            # Fields to request
            args = {
                'title__contains': form.cleaned_data['search_plant'],
                'category': form.cleaned_data['search_category'],
                'shade': form.cleaned_data['search_shade'],
                'moisture': form.cleaned_data['search_moisture'],
                'wind': form.cleaned_data['search_wind'],
                'soil': form.cleaned_data['search_soil'],
                'growth_rate': form.cleaned_data['search_growth_rate']
            }
            for key in args.copy():
                item = args.get(key)
                if item is None:
                    args.pop(key)
                if type(item) == str and item is not None and len(item) == 0:
                    args.pop(key)

            # Query all plants
            if len(args) == 0:
                plants = []
            else:
                plants = Plant.objects.filter(**args).all()
            pagePlant = Paginate.getPaginate(request, plants)

    else:
        pagePlant = Paginate.getPaginate(request)
        form = PlantFilterForm()
    return render(request, 'plant/plant/index.html', {'pagePlant': pagePlant, 'form': form})


def detail(request, plant_slug: str):
    plant = get_object_or_404(Plant, slug=plant_slug)
    # Get plants by category
    plants_by_category = Plant.objects.filter(category=plant.category) \
        .exclude(id=plant.id) \
        .order_by('id') \
        .all()[:3]
    # Get plants related
    plants_related = related_plants(plant)
    return render(request, 'plant/plant/detail.html', {
        'plant': plant,
        'plants_by_category': plants_by_category,
        'plants_related': plants_related
    })

def related_plants(plant: Plant):
    description_current = plant.description

    plants_related = Plant.objects.filter(description__in=description_current).exclude(id=plant.id)
    plants_related = plants_related.annotate(some_description=Count('description'))
    return plants_related.order_by('id')[:3]
