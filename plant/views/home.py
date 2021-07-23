from django.shortcuts import render

from plant.models import Plant


def index(request):
    plants = Plant.objects.order_by('id')[:3]
    return render(request, 'plant/index.html', {'plants': plants})
