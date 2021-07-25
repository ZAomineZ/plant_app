from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from admin.tests.utils.Message import Message
from plant import factories
from plant.models import FavoritePlant


class FavoritePlantAction(TestCase):
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
        self.user = User.objects.create(username='Vincent', email='vincent@test.fr')
        self.user.set_password('test')
        self.user.save()
        self.user_fake = factories.UserFactory.create(username='Toto', email='toto@test.fr', password='testtoto')

    def test_action_add_to_favorite_plant_with_bad_user_authenticated(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.add', args=(self.user_fake.username, self.plant.slug)))
        self.assertEqual(response.status_code, 302)

    def test_action_add_to_favorite_plant_with_user_not_authenticated(self):
        response = self.client.get(reverse('plant:favorite_plant.add', args=(self.user_fake.username, self.plant.slug)))
        self.assertEqual(response.status_code, 302)

    def test_action_add_to_favorite_plant_with_bad_plant(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.add', args=(self.user.username, 'plant-test')))
        self.assertEqual(response.status_code, 404)

    def test_action_add_to_favorite_plant(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.add', args=(self.user.username, self.plant.slug)))

        plants_favorite = FavoritePlant.objects.all()
        plant_favorite = plants_favorite[0]
        self.assertEqual(response.status_code, 302)
        self.assertEqual(plant_favorite.user, self.user)
        self.assertEqual(plant_favorite.plant, self.plant)
        self.assertEqual(FavoritePlant.objects.count(), 1)

    def test_action_add_to_favorite_plant_exist(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')
        # Create favorite_plant to user current and to plant current
        FavoritePlant.objects.create(user=self.user, plant=self.plant)

        response = self.client.get(reverse('plant:favorite_plant.add', args=(self.user.username, self.plant.slug)))

        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous avez déjà ajouté cette plante dans vos favoris !', messages)

    def test_action_remove_to_favorite_plant_with_bad_user_authenticated(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(
            reverse('plant:favorite_plant.delete', args=(self.user_fake.username, self.plant.slug)))
        self.assertEqual(response.status_code, 302)

    def test_action_delete_to_favorite_plant_with_user_not_authenticated(self):
        response = self.client.get(
            reverse('plant:favorite_plant.delete', args=(self.user_fake.username, self.plant.slug)))
        self.assertEqual(response.status_code, 302)

    def test_action_delete_to_favorite_plant_with_bad_plant(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.delete', args=(self.user.username, 'plant-test')))
        self.assertEqual(response.status_code, 404)

    def test_action_delete_to_favorite_plant(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')
        # Create favorite_plant to user current and to plant current
        FavoritePlant.objects.create(user=self.user, plant=self.plant)

        response = self.client.get(reverse('plant:favorite_plant.delete', args=(self.user.username, self.plant.slug)))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(FavoritePlant.objects.count(), 0)

    def test_action_add_to_favorite_plant_dont_exist(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:favorite_plant.delete', args=(self.user.username, self.plant.slug)))

        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous ne pouvez pas supprimier une plante qui n\'est pas dans vos favoris !', messages)
