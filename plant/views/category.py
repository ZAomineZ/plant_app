from django.shortcuts import render, get_object_or_404

from plant.models import Category, Plant
from plant.views.utils import Paginate


def categories(request):
    categories = Category.objects.all()
    return render(request, 'plant/category/index.html', {'categories': categories})


def category_detail(request, category_slug: str):
    category = get_object_or_404(Category, slug=category_slug)
    # Get all plants with the paginator
    plants = Plant.objects.filter(category=category).all()
    pagePlant = Paginate.getPaginate(request, plants)
    return render(request, 'plant/category/detail.html', {'category': category, 'pagePlant': pagePlant})
