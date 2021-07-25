from django.contrib.auth.models import User
from django.test import Client


class Authentication:
    @staticmethod
    def authenticated_user(user: User) -> None:
        client = Client()
        client.login(username=user.username, password='test')
