from django.test import TestCase
from django.urls import reverse

from plant.models import CustomUser


class LoginPageTest(TestCase):
    def setUp(self) -> None:
        # Create user factory
        self.user = CustomUser.objects.create(username='Vincent', email='vincent@test.fr')
        self.user.set_password('test')
        self.user.save()

    def test_login_page_with_user_authenticated(self):
        # Authenticated user
        self.client.login(username='Vincent', password='test')

        response = self.client.get(reverse('plant:auth.login'))
        self.assertEqual(response.status_code, 302)

    def test_login_page_with_user_dont_authenticated(self):
        response = self.client.get(reverse('plant:auth.login'))
        self.assertEqual(response.status_code, 200)
