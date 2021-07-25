from django.test import TestCase
from django.urls import reverse

from plant import factories
from plant.models import CustomUser, FavoritePlant


class FavoritePlantIndexPage(TestCase):
    def setUp(self) -> None:
        # Create category factory
        category = factories.CategoryFactory.create(title='Vivace', slug='vivace',
                                                    description='Je suis une description de test')
        # Create plant factory
        self.plant = factories.PlantFactory.create(title='Armoise', slug='armoise',
                                                   description='Je suis une description.',
                                                   category=category, shade='Plein ombre', moisture='Sol sec',
                                                   wind='Exposition maritime', soil='Argile lourde', growth_rate='Vite')

        # Create user factory
        self.user = CustomUser.objects.create(username='Vincent', email='vincent@test.fr')
        self.user.set_password('test')
        self.user.save()
        self.user_fake = factories.UserFactory.create(username='Toto', email='toto@test.fr', password='testtoto')
        # Create favorite_plant factory
        favorite_plant = FavoritePlant.objects.create(plant=self.plant)
        self.user.favorite_plants.add(favorite_plant)

    def test_index_page_with_bad_user(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.index', args=('damien',)))
        self.assertEqual(response.status_code, 404)

    def test_index_page_with_bad_user_authenticated(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.index', args=(self.user_fake.username,)))
        self.assertEqual(response.status_code, 302)

    def test_index_page_with_any_favorite_plant(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        self.plant.delete()
        response = self.client.get(reverse('plant:favorite_plant.index', args=(self.user.username,)))

        plants_favorite = response.context['plants_favorite']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(plants_favorite), 0)

    def test_index_page_with_user_not_authenticated(self):
        response = self.client.get(reverse('plant:favorite_plant.index', args=(self.user_fake.username,)))

        self.assertEqual(response.status_code, 302)

    def test_index_page(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.index', args=(self.user.username,)))

        plants_favorite = response.context['plants_favorite']
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(plants_favorite), 1)
