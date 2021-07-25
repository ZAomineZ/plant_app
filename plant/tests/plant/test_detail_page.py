from django.test import TestCase
from django.urls import reverse

from plant import factories


class PlantDetailPage(TestCase):
    def setUp(self) -> None:
        category = factories.CategoryFactory.create(title='Vivace', slug='vivace',
                                                    description='Je suis une description de test')

        self.plant = factories.PlantFactory.create(title='Armoise', slug='armoise',
                                                   description='Je suis une description.',
                                                   category=category, shade='Plein ombre', moisture='Sol sec',
                                                   wind='Exposition maritime', soil='Argile lourde', growth_rate='Vite')
        factories.PlantFactory.create(title='Arbre de Jade', slug='arbre-de-jade',
                                      description='Je suis une description............................',
                                      category=category, shade='Plein ombre', moisture='Sol sec',
                                      wind='Exposition maritime', soil='Argile lourde', growth_rate='Vite')
        factories.PlantFactory.create_batch(4)

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

    def test_detail_page_with_plants_like_category(self):
        response = self.client.get(reverse('plant:plants.detail', args=(self.plant.slug,)))

        plants_by_category = response.context['plants_by_category']
        titles = self.getTitles(plants_by_category)
        self.assertEqual(len(plants_by_category), 1)
        self.assertTrue(len(plants_by_category) <= 3)
        self.assertNotIn(self.plant.title, titles)

    def test_detail_page_with_plants_related(self):
        response = self.client.get(reverse('plant:plants.detail', args=(self.plant.slug,)))

        plants_related = response.context['plants_related']
        titles = self.getTitles(plants_related)
        self.assertEqual(len(plants_related), 1)
        self.assertTrue(len(plants_related) >= 3)
        self.assertNotIn(self.plant.title, titles)

    def getTitles(self, plants) -> list:
        titles = []
        for plant in plants:
            titles.append(plant.title)
        return titles
