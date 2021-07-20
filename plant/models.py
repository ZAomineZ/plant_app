from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()

    def __str__(self):
        return self.title


class Plant(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.OneToOneField("ImagePlant", on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class ImagePlant(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title
