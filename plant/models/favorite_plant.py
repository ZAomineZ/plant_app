from django.db import models

from plant.models.plant import Plant


class FavoritePlant(models.Model):
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)