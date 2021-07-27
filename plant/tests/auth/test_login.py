from django.test import TestCase
from django.urls import reverse

from admin.tests.utils.Message import Message
from plant.models import CustomUser


class LoginTest(TestCase):
    def setUp(self) -> None:
        # Create user factory
        self.user = CustomUser.objects.create(username='Vincent', email='vincent@test.fr')
        self.user.set_password('test')
        self.user.save()

    def test_register_form_invalid(self):
        response = self.request_login({
            'username': '',
            'password': 'test'
        })
        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Le formulaire n\'est pas valide', messages)

    def test_login_with_username_dont_exist(self):
        response = self.request_login({
            'username': 'John',
            'password': 'testdetest'
        })
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], 'Cette username n\'éxiste pas dans notre base de donnée')

    def test_login_with_success(self):
        response = self.request_login({
            'username': 'Vincent',
            'password': 'test'
        })
        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 302)
        self.assertIn('Vous êtes maitenant connecté', messages)
        self.assertTrue(self.user.is_authenticated)

    def request_login(self, args: dict = None):
        response = self.client.post(reverse('plant:auth.login'), data=args)
        return response
