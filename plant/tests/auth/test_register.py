from django.test import TestCase
from django.urls import reverse

from admin.tests.utils.Message import Message
from plant.models import CustomUser


class RegisterTest(TestCase):
    def setUp(self) -> None:
        # Create user factory
        self.user = CustomUser.objects.create(username='Vincent', email='vincent@test.fr')
        self.user.set_password('test')
        self.user.save()

    def test_register_form_invalid(self):
        response = self.request_register({
            'username': 'lol',
            'email': 'lol',
            'password': 'test',
            'password_confirm': 'loelel'
        })
        messages = Message.getMessages(response)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Le formulaire n\'est pas valide', messages)

    def test_register_with_username_exist(self):
        response = self.request_register({
            'username': 'Vincent',
            'email': 'email@email.fr',
            'password': 'testdetest',
            'password_confirm': 'testdetest'
        })
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['username'][0], 'L\'username est dèjà pris')

    def test_register_with_email_exist(self):
        response = self.request_register({
            'username': 'Toto',
            'email': 'vincent@test.fr',
            'password': 'testdetest',
            'password_confirm': 'testdetest'
        })
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['email'][0], 'L\'email est dèjà pris')

    def test_register_with_password_and_password_confirm_no_identical(self):
        response = self.request_register({
            'username': 'Toto',
            'email': 'vincent@test.fr',
            'password': 'testdetest',
            'password_confirm': 'test'
        })
        form = response.context['form']
        self.assertEqual(response.status_code, 200)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['password'][0], 'Vos mot de passes doivent être identiques.')

    def test_register_check_password_hash(self):
        response = self.request_register({
            'username': 'Toto',
            'email': 'toto@test.fr',
            'password': 'testdetest',
            'password_confirm': 'testdetest'
        })
        user = CustomUser.objects.filter(username='Toto').first()
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.check_password('testdetest'))

    def test_register_with_success(self):
        response = self.request_register({
            'username': 'Toto',
            'email': 'toto@test.fr',
            'password': 'testdetest',
            'password_confirm': 'testdetest'
        })
        user = CustomUser.objects.filter(username='Toto').first()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(user.email, 'toto@test.fr')
        self.assertEqual(user.username, 'Toto')

    def request_register(self, args: dict = None):
        response = self.client.post(reverse('plant:auth.register'), data=args)
        return response
