from django.test import TestCase
from django.urls import reverse

from admin.tests.utils.Message import Message
from plant import factories
from plant.models import Category


class CategoryDelete(TestCase):
    def setUp(self) -> None:
        # Create a category with the current factory
        self.category = factories.CategoryFactory.create(
            title="Vivace",
            slug="vivace",
            description="Je suis une description pour la plate 'Vivace'"
        )

    def test_delete_category_with_bad_category(self):
        response = self.request_delete_category(200)

        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous ne pouvez pas supprimer une catégorie qui n\'éxiste pas', messages)

    def test_delete_category_with_good_category(self):
        response = self.request_delete_category(self.category.id)

        messages = Message.getMessages(response)
        category = Category.objects.filter(pk=self.category.id).first()
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous avez supprimé cette catégorie avec success', messages)
        self.assertIsNone(category)

    def request_delete_category(self, category_id: int):
        return self.client.get(reverse('admin:categories.delete', args=(category_id,)))
