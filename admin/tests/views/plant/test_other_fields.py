from django.test import TestCase
from django.urls import reverse

from admin.tests.utils import File
from admin.views.utils.Dict import Dict
from plant import factories
from plant.models import Category, Plant


class PlantCreateWithOtherFields(TestCase):
    def setUp(self) -> None:
        factories.CategoryFactory.create(
            title="Vivace",
            slug="vivace",
            description="Je suis une description pour la plate 'Vivace'"
        )

    def test_create_with_shade(self):
        response = self.requestCreatePlant('hortensia', {'shade': 'semi-ombre'})

        plantLast = Plant.objects.filter(slug='hortensia').last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check field shad is not None
        self.assertEqual(plantLast.shade, 'semi-ombre')
        self.assertIsNotNone(plantLast.shade)

    def test_create_with_moisture(self):
        response = self.requestCreatePlant('hortensia', {'moisture': 'sol-sec'})

        plantLast = Plant.objects.filter(slug='hortensia').last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check field shad is not None
        self.assertEqual(plantLast.moisture, 'sol_sec')
        self.assertIsNotNone(plantLast.moisture)

    def test_create_with_wind(self):
        response = self.requestCreatePlant('hortensia', {'wind': 'exposition-maritime'})

        plantLast = Plant.objects.filter(slug='hortensia').last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check field shad is not None
        self.assertEqual(plantLast.wind, 'exposition-maritime')
        self.assertIsNotNone(plantLast.wind)

    def test_create_with_soil(self):
        response = self.requestCreatePlant('hortensia', {'soil': 'moyen'})

        plantLast = Plant.objects.filter(slug='hortensia').last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check field shad is not None
        self.assertEqual(plantLast.soil, 'moyen')
        self.assertIsNotNone(plantLast.soil)

    def test_create_with_growth_rate(self):
        response = self.requestCreatePlant('hortensia', {'growth-rate': 'lent'})

        plantLast = Plant.objects.filter(slug='hortensia').last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check field shad is not None
        self.assertEqual(plantLast.growth_rate, 'lent')
        self.assertIsNotNone(plantLast.growth_rate)

    def test_create_with_many_fields(self):
        response = self.requestCreatePlant('hortensia', {
            'growth_rate': 'lent',
            'wind': 'exposition-maritime',
            'soil': 'moyen'
        })

        plantLast = Plant.objects.filter(slug='hortensia').last()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check field shad is not None
        self.assertEqual(plantLast.growth_rate, 'lent')
        self.assertEqual(plantLast.wind, 'exposition-maritime')
        self.assertEqual(plantLast.soil, 'moyen')
        self.assertIsNotNone(plantLast.growth_rate)
        self.assertIsNotNone(plantLast.wind)
        self.assertIsNotNone(plantLast.soil)

        # Check if the other fields are None
        self.assertTrue(plantLast.shade == '')
        self.assertTrue(plantLast.moisture == '')

    def requestCreatePlant(self, slug: str, argsFields: dict):
        category = Category.objects.get(slug='vivace')
        args = {
            'title': 'Hortensia',
            'slug': slug,
            'description': 'Je suis une description pour la plante "Hortensia"',
            'category': category.id,
            'image': File.generateImage()
        }
        args = Dict.merge_two_dicts(args, argsFields)

        return self.client.post(reverse('admin:plants.create'), data=args, format='multipart')
