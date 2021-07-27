from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

from plant.models.favorite_plant import FavoritePlant


class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str = None):
        if not username:
            raise ValueError('Users must have and a username')

        user = self.model(email=self.normalize_email('vincentcapek@gmail.com'))
        user.username = username
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str = None):
        user = self.create_user(
            username=username,
            password=password
        )
        user.admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    username = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, unique=True, default="SOME EMAIL")
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)  # a superuser
    favorite_plants = models.ManyToManyField(FavoritePlant)

    objects = UserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    @property
    def is_admin(self):
        return self.admin
