from django.test import TestCase
from django.urls import reverse

from plant import factories


class PlantDetailPage(TestCase):
    def setUp(self) -> None:
        category = factories.CategoryFactory.create(title='Vivace', slug='vivace',
                                                    description='Je suis une description de test')

        self.plant = factories.PlantFactory.create(title='Armoise', slug='armoise',
                                                   description='Je suis une description de test',
                                                   category=category, shade='Plein ombre', moisture='Sol sec',
                                                   wind='Exposition maritime', soil='Argile lourde', growth_rate='Vite')

    def test_detail_page_with_good_status(self):
        response = self.client.get(reverse('plant:plants.detail', args=(self.plant.slug,)))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_with_good_plant_param(self):
        response = self.client.get(reverse('plant:plants.detail', args=(self.plant.slug,)))

        plant = response.context['plant']
        self.assertEqual(plant.title, 'Armoise')
        self.assertIsNotNone(plant)

    def test_detail_page_with_bad_plant_param(self):
        response = self.client.get(reverse('plant:plants.detail', args=('test-de-test',)))
        self.assertEqual(response.status_code, 404)
