from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseRedirect
from django.shortcuts import render

from plant.models import Plant, Category, CustomUser


@user_passes_test(lambda u: u.is_admin)
def index(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        userCurrent = CustomUser.objects.filter(email=email).first()
        user = authenticate(request, username=userCurrent.username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            return HttpResponseRedirect('/superadmin')

    plantsNumber = Plant.objects.count()
    categoriesNumber = Category.objects.count()
    return render(request, 'admin/index.html', {
        'plantsNumber': plantsNumber,
        'categoriesNumber': categoriesNumber
    })
