from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import path
from . import views

app_name = 'plant'
urlpatterns = [
    path('', views.home.index, name="index"),
    path('plants/', views.plant.index, name="plants.index"),
    path('plants/<str:plant_slug>', views.plant.detail, name="plants.detail"),
    path('categories/', views.category.categories, name="categories"),
    path('categories/<str:category_slug>', views.category.category_detail, name="category.detail"),
    path('favorite_plant/<str:username>', views.favorite_plant.index, name="favorite_plant.index"),
    path('favorite_plant/<str:username>/add/<str:plant_slug>', views.favorite_plant.add, name="favorite_plant.add"),
    path('favorite_plant/<str:username>/delete/<str:plant_slug>', views.favorite_plant.delete, name="favorite_plant.delete")
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
