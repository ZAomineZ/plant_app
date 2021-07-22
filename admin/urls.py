from django.urls.conf import path

from . import views

app_name = 'admin'
urlpatterns = [
    path('', views.index, name="index"),
    # URLS Plant MODEL
    path('plants/', views.plants, name="plants"),
    path('plants/create', views.plant_create, name="plants.create"),
    path('plants/edit/<int:plant_id>', views.plant_edit, name="plants.edit"),
    # URLS Category MODEL
    path('categories/', views.categories, name="categories"),
    path('categories/create', views.categories_create, name="categories.create"),
    path('categories/edit/<int:category_id>', views.categories_edit, name="categories.edit")
]
