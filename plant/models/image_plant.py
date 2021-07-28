from django.db import models


class ImagePlant(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images')

    @property
    def get_image(self):
        return '/plant/media/' + self.image.name

    def __str__(self):
        return self.title
