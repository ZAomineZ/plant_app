import io
import os
from pathlib import Path

from PIL import Image
from django.test import TestCase
from django.urls import reverse

from PlantApp import settings
from admin.tests.utils.Message import Message
from plant import factories
from plant.models import Plant, Category


# Create your tests here.

# Index Page plant model
class PlantIndexPageTestCase(TestCase):
    def setUp(self) -> None:
        factories.CategoryFactory.create_batch(2)
        factories.PlantFactory.create_batch(6)

    def test_index_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:plants'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_with_plants(self):
        self.assertEqual(Plant.objects.count(), 6)


# Create Page plant model
def removeAllImages():
    path = str(Path(__file__).parent.parent.parent.parent) + (settings.MEDIA_URL + 'images')
    if Path(path).is_dir():
        os.chmod(path, 0o777)
        files = os.listdir(path)
        for file in files:
            print(path + '/' + file)
            os.remove(path + '/' + file)
        os.rmdir(path)


class PlantCreatePageTestCase(TestCase):
    def setUp(self) -> None:
        removeAllImages()
        factories.CategoryFactory.create(
            title="Vivace",
            slug="vivace",
            description="Je suis une description pour la plate 'Vivace'"
        )

    def tearDown(self) -> None:
        removeAllImages()

    def test_create_plant_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:categories.create'))
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
            os.path.exists(str(Path(__file__).parent.parent.parent.parent) + settings.MEDIA_URL + 'test.png'))

    def requestCreatePlant(self, slug: str):
        category = Category.objects.get(slug='vivace')
        args = {
            'title': 'Hortensia',
            'slug': slug,
            'description': 'Je suis une description pour la plante "Hortensia"',
            'category': category.id,
            'image': self.generateImage()
        }
        return self.client.post(reverse('admin:plants.create'), data=args, format='multipart')

    def generateImage(self):
        file = io.BytesIO()
        image = Image.new("RGBA", size=(50, 50), color=(256, 0, 0))
        image.save(file, "png")
        file.seek(0)
        file.name = "images/test.png"
        return file
