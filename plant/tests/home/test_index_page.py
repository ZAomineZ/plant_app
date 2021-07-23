import time

from django.test import TestCase
from django.urls import reverse

from plant import factories


class HomeIndexPage(TestCase):
    def setUp(self) -> None:
        category = factories.CategoryFactory.create(title='Vivace', slug='vivace',
                                                    description='Je suis une description de test')

        factories.PlantFactory.create(title='Asiminier', slug='asiminier',
                                      description='Je suis une description de test', category=category,
                                      shade='Plein ombre', moisture='Sol sec', wind='Exposition maritime',
                                      soil='Argile lourde', growth_rate='Vite')
        time.sleep(2)
        factories.PlantFactory.create(title='Armoise', slug='armoise',
                                      description='Je suis une description de test', category=category,
                                      shade='Plein ombre', moisture='Sol sec', wind='Exposition maritime',
                                      soil='Argile lourde', growth_rate='Vite')

    def test_index_page_with_good_status_code(self):
        response = self.client.get(reverse('plant:index'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_with_plants(self):
        response = self.client.get(reverse('plant:index'))

        plants = response.context['plants']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(plants), 2)
        self.assertTrue(len(plants) <= 3)

    def test_index_page_with_plants_by_created_at(self):
        response = self.client.get(reverse('plant:index'))

        plants = response.context['plants']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(plants[0].title, 'Asiminier')
        self.assertEqual(plants[1].title, 'Armoise')
