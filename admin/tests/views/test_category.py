from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse

from plant import factories
from plant.models import Category


# Index Page Category model
class CategoryIndexPageTestCase(TestCase):
    def setUp(self) -> None:
        factories.CategoryFactory.create_batch(2)

    def test_index_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:plants.create'))
        self.assertEqual(response.status_code, 200)

    def test_index_page_with_categories(self):
        self.assertEqual(Category.objects.count(), 2)


class CategoryCreatePageTestCase(TestCase):
    def test_create_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:categories.create'))
        self.assertEqual(response.status_code, 200)

    def test_create_page_with_post_without_slug(self):
        response = self.requestCreateCategory('')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 0)
        self.assertTrue('This field is required.' in response.context['errors']['slug'])

    def test_create_page_with_method_with_bad_slug(self):
        response = self.requestCreateCategory("Herbacé")

        categoryLast = Category.objects.filter(slug="herbace").get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        # Check fields to category model
        self.assertEqual(categoryLast.slug, 'herbace')

    def test_create_page_with_method_post(self):
        response = self.requestCreateCategory("herbacé")

        categoryLast = Category.objects.filter(slug="herbace").get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        # Check fields to category model
        self.assertEqual(categoryLast.title, 'Herbacé')
        self.assertEqual(categoryLast.slug, 'herbace')
        self.assertEqual(categoryLast.description, 'Je suis une description pour le title "Herbacé"')

    def test_create_page_with_message_flash(self):
        response = self.requestCreateCategory("herbacé")
        messages = []
        for message in get_messages(response.wsgi_request):
            messages.append(str(message))
        self.assertIn('Tu as crée ta catégorie avec success !', messages)

    def requestCreateCategory(self, slug: str):
        args = {
            'title': 'Herbacé',
            'slug': slug,
            'description': 'Je suis une description pour le title "Herbacé"'
        }
        return self.client.post(reverse('admin:categories.create'), data=args)


class CategoryEditPageTestCase(TestCase):
    def setUp(self) -> None:
        factories.CategoryFactory.create(title="Herbacé", slug="herbace", description="Je suis une description de test")
        self.category = Category.objects.filter(slug="herbace").get()

    def test_edit_page_with_good_status_code(self):
        response = self.client.get(reverse('admin:categories.edit', args=(self.category.id,)))
        self.assertEqual(response.status_code, 200)

    def test_create_page_with_post_without_slug(self):
        response = self.requestEditCategory('')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 1)
        self.assertTrue('This field is required.' in response.context['errors']['slug'])

    def test_create_page_with_method_with_bad_slug(self):
        response = self.requestEditCategory("Vivace")

        categoryLast = Category.objects.filter(slug="vivace").get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        # Check fields to category model
        self.assertEqual(categoryLast.slug, 'vivace')

    def test_create_page_with_method_post(self):
        response = self.requestEditCategory("vivace")

        categoryLast = Category.objects.filter(slug="vivace").get()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Category.objects.count(), 1)
        # Check fields to category model
        self.assertEqual(categoryLast.title, 'Vivace')
        self.assertEqual(categoryLast.slug, 'vivace')
        self.assertEqual(categoryLast.description, 'Je suis une description pour le title "Vivace"')

    def test_create_page_with_message_flash(self):
        response = self.requestEditCategory("vivace")
        messages = []
        for message in get_messages(response.wsgi_request):
            messages.append(str(message))
        self.assertIn('Tu as édité ta catégorie avec success !', messages)

    def requestEditCategory(self, slug: str):
        args = {
            'title': 'Vivace',
            'slug': slug,
            'description': 'Je suis une description pour le title "Vivace"'
        }
        return self.client.post(reverse('admin:categories.edit', args=(self.category.id,)), data=args)
