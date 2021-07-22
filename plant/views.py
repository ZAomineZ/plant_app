from django.core.paginator import Paginator
from django.shortcuts import render

from plant.models import Plant


# Create your views here.
def index(request):
    plants = Plant.objects.all()
    paginator = Paginator(plants, 9)

    page_number = request.GET.get('page')
    pagePlant = paginator.get_page(page_number)
    return render(request, 'plant/index.html', {'pagePlant': pagePlant})
