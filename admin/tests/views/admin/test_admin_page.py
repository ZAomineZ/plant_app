from django.test import TestCase
from django.urls import reverse


class PageAdminPage(TestCase):
    def setUp(self) -> None:
        pass

    def test_admin_page_with_user_no_is_admin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 302)

    def test_admin_page_with_user_is_admin(self):
        response = self.client.get(reverse('admin:index'))
        self.assertEqual(response.status_code, 200)
