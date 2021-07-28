import os

from django.db import models

from plant.models.category import Category
from plant.models.image_plant import ImagePlant


class Plant(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    shade = models.CharField(max_length=50, null=True)
    moisture = models.CharField(max_length=50, null=True)
    wind = models.CharField(max_length=50, null=True)
    soil = models.CharField(max_length=50, null=True)
    growth_rate = models.CharField(max_length=50, null=True)

    image = models.OneToOneField(ImagePlant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
