from django.urls.conf import path

from . import views

app_name = 'admin'
urlpatterns = [
    path('', views.index, name="admin.index"),
    path('plants/', views.plants, name="admin.plants"),
    path('plants/create', views.plant_create, name="admin.plants.create")
]
