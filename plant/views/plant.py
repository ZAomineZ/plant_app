from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
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
