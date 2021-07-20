from django.urls.conf import path

from . import views

app_name = 'admin'
urlpatterns = [
    path('', views.index, name="index"),
    # URLS Plant MODEL
    path('plants/', views.plants, name="plants"),
    path('plants/create', views.plant_create, name="plants.create"),
    # URLS Category MODEL
    path('categories/', views.categories, name="categories"),
    path('categories/create', views.categories_create, name="categories.create"),
]
