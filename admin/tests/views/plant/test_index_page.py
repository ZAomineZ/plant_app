from django.test import TestCase
from django.urls import reverse

from plant import factories
from plant.models import Plant


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
