from django.contrib.auth.models import User
from django.db import models


# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title


class ImagePlant(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title


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


class FavoritePlant(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class CustomUser(User):
    favorite_plants = models.ManyToManyField(FavoritePlant)

    def __str__(self):
        return self.username
