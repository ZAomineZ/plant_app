from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=60)
    slug = models.CharField(max_length=60)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title
