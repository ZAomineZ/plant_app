from django.test import TestCase
from django.urls import reverse

from plant import factories
from plant.models import Category


# Index Page Category model
class CategoryIndexPageTestCase(TestCase):
    def setUp(self) -> None:
        factories.CategoryFactory.create_batch(2)

    def test_index_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:categories.create'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_with_categories(self):
        self.assertEqual(Category.objects.count(), 2)
