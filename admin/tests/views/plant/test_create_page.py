import os
from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from PlantApp import settings
from admin.tests.utils import File
from admin.tests.utils.Message import Message
from plant import factories
from plant.models import Plant, Category


# Create your tests here.
class PlantCreatePageTestCase(TestCase):
    def setUp(self) -> None:
        File.removeAllImages()
        factories.CategoryFactory.create(
            title="Vivace",
            slug="vivace",
            description="Je suis une description pour la plate 'Vivace'"
        )

    def tearDown(self) -> None:
        File.removeAllImages()

    def test_create_plant_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:plants.create'))
        self.assertEqual(response.status_code, 200)

    def test_create_plant_page_with_method_post_without_slug(self):
        response = self.requestCreatePlant('')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Plant.objects.count(), 0)
        self.assertTrue('This field is required.' in response.context['errors']['slug'])

    def test_create_plant_page_with_method_post_with_bad_slug(self):
        response = self.requestCreatePlant("Hortensia")

        plantLast = Plant.objects.filter(slug="hortensia").get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Plant.objects.count(), 1)
        # Check fields to category model
        self.assertEqual(plantLast.slug, 'hortensia')

    def test_create_plant_page_with_method_post(self):
        response = self.requestCreatePlant("hortensia")

        plantLast = Plant.objects.filter(slug="hortensia").get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        # Check fields to category model
        self.assertEqual(plantLast.title, 'Hortensia')
        self.assertEqual(plantLast.slug, 'hortensia')
        self.assertEqual(plantLast.description, 'Je suis une description pour la plante "Hortensia"')
        self.assertEqual(plantLast.category.title, 'Vivace')

    def test_create_plant_page_with_method_post_and_message_flash(self):
        response = self.requestCreatePlant("hortensia")
        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        self.assertIn('Vous avez crée une plante avec succès !', messages)

    def test_create_plant_page_with_method_post_and_file_uploaded(self):
        response = self.requestCreatePlant("hortensia")
        # Check image uploaded
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            os.path.exists(str(Path(
                __file__).parent.parent.parent.parent.parent) + '/plant/static/plant' + settings.MEDIA_URL + 'test.png'))

    def requestCreatePlant(self, slug: str):
        category = Category.objects.get(slug='vivace')
        args = {
            'title': 'Hortensia',
            'slug': slug,
            'description': 'Je suis une description pour la plante "Hortensia"',
            'category': category.id,
            'image': File.generateImage()
        }
        return self.client.post(reverse('admin:plants.create'), data=args, format='multipart')
