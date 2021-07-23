from django.core.paginator import Paginator

from plant.models import Plant


def getPaginate(request, plants: list = None):
    if plants is None:
        items = Plant.objects.all()
    else:
        items = plants
    paginator = Paginator(items, 9)

    page_number = request.GET.get('page')
    return paginator.get_page(page_number)
