import os
from pathlib import Path

from django.test import TestCase
from django.urls import reverse

from PlantApp import settings
from admin.tests.utils.Message import Message
from plant import factories
from plant.models import Category, ImagePlant


class DeletePlantTest(TestCase):
    def setUp(self) -> None:
        # Create a category with the current factory
        factories.CategoryFactory.create(
            title="Vivace",
            slug="vivace",
            description="Je suis une description pour la plate 'Vivace'"
        )
        # Create a plant with the current factory
        self.image = factories.ImageFactory.create(
            title='Test'
        )
        self.plant = factories.PlantFactory.create(
            title="Armoise",
            slug="armoise",
            description="Je suis une description de test",
            category=Category.objects.filter(slug='vivace').first(),
            image=ImagePlant.objects.filter(title='Test').first()
        )

    def test_action_delete_with_bad_plant(self):
        response = self.request_delete_plant(200)

        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous ne pouvez pas supprimer une plant qui n\'éxiste pas', messages)

    def test_action_delete_with_good_plant(self):
        response = self.request_delete_plant(self.plant.id)

        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous avez supprimé cette plant avec success', messages)

    def test_action_delete_with_unlink_image_current(self):
        response = self.request_delete_plant(self.plant.id)

        image = ImagePlant.objects.filter(title=self.image.title).first()
        self.assertEqual(response.status_code, 302)
        self.assertFalse(
            os.path.exists(str(Path(
                __file__).parent.parent.parent.parent.parent) + '/plant/static/plant' + settings.MEDIA_URL + str(self.plant.image.image)))
        self.assertIsNone(image)

    def request_delete_plant(self, plant_id: int = None):
        return self.client.get(reverse('admin:plants.delete', args=(plant_id,)))
