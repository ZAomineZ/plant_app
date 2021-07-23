from django.test import TestCase
from django.urls import reverse

from admin.tests.utils.Message import Message
from plant import factories
from plant.models import Category


class TestFilterPlant(TestCase):
    def setUp(self) -> None:
        # Create factory to category model
        self.category: Category = factories.CategoryFactory.create(title='Vivace', slug='vivace',
                                                                   description='description de test')
        factories.PlantFactory.create(
            title='Bananier', slug='bananier', description='description de test',
            category=self.category, shade='Plein ombre', moisture='Sol sec', wind='Exposition maritime',
            soil='Argile lourde', growth_rate='Vite'
        )
        factories.PlantFactory.create(
            title='Orpin de Morgane', slug='orpin-de-morgane', description='description de test',
            category=self.category, shade='Semi ombre', moisture='Sol humide', wind='Tolèrant au vent fort',
            soil='Moyen', growth_rate='Lent'
        )
        factories.PlantFactory.create(
            title='Arbre de Jade', slug='arbre-de-jade', description='description de test',
            category=self.category, shade='Plein soleil', moisture='Sol sec', wind='Exposition maritime',
            soil='Sol pauvre', growth_rate='Moyen'
        )

    def test_filter_plant_with_all_empty_fields(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 0)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_plant_with_full_word(self):
        request = self.requestFilter({
            'search_plant': 'Bananier',
            'search_category': '',
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 1)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_plant_with_dont_full_word(self):
        request = self.requestFilter({
            'search_plant': 'Banani',
            'search_category': '',
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 1)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_category(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': self.category.id,
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 3)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_category_with_dont_exist_category(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': 150,
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })

        messages = Message.getMessages(response=request)
        self.assertIn('Cette catégorie n\'est pas présente dans notre base de donnée !', messages)
        self.assertEqual(request.status_code, 302)

    def test_filter_search_shape(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': 'Plein ombre',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 1)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_moisture(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': 'Sol sec',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 2)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_wind(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': '',
            'search_wind': 'Exposition maritime',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 2)
        self.assertEqual(request.status_code, 200)

    def test_filter_search_soil(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': 'Moyen',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 1)
        self.assertEqual(request.status_code, 200)

    def test_filter_growth_rate(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': '',
            'search_wind': '',
            'search_soil': '',
            'search_growth_rate': 'Vite'
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 1)
        self.assertEqual(request.status_code, 200)

    def test_filter_with_many_fields(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': 'Sol sec',
            'search_wind': 'Exposition maritime',
            'search_soil': '',
            'search_growth_rate': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 2)
        self.assertEqual(request.status_code, 200)

    def test_reset_filter(self):
        request = self.requestFilter({
            'search_plant': '',
            'search_category': '',
            'search_shade': '',
            'search_moisture': 'Sol sec',
            'search_wind': 'Exposition maritime',
            'search_soil': '',
            'search_growth_rate': '',
            'reset_filter': ''
        })
        plants = request.context['pagePlant']

        self.assertEqual(len(plants), 3)
        self.assertEqual(request.status_code, 200)

    def requestFilter(self, args: dict):
        return self.client.get(reverse('plant:plants.index'), data=args)
