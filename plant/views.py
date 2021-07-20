from django.shortcuts import render


# Create your views here.
def index(request):
    context = {'plants': [0, 0, 0, 0, 0, 0]}
    return render(request, 'plant/index.html', context)
