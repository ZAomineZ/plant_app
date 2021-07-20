from django.urls.conf import path
from . import views

app_name = 'plant'
urlpatterns = [
    path('', views.index, name="index")
]
