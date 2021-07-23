from django.urls.conf import path
from . import views

app_name = 'plant'
urlpatterns = [
    path('', views.index, name="index"),
    path('categories/', views.categories, name="categories"),
    path('categories/<str:category_slug>', views.category_detail, name="category.detail")
]
