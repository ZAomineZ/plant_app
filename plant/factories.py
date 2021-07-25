import factory
from django.core.files.base import ContentFile

from plant.models import Plant, Category, ImagePlant, FavoritePlant, CustomUser


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser
        django_get_or_create = ('username', 'email', 'password', 'is_superuser')

    username = factory.sequence(lambda n: 'Title %s' % n)
    email = factory.sequence(lambda n: 'email%s.test.fr' % n)
    password = 'test'
    is_superuser = False


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        django_get_or_create = ('title', 'slug', 'description')

    title = factory.sequence(lambda n: 'Title %s' % n)
    slug = factory.LazyAttribute(lambda o: o.title)
    description = factory.sequence(lambda n: 'Je suis une description : %s' % n)


class ImageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ImagePlant
        django_get_or_create = ('title', 'image')

    title = factory.sequence(lambda n: 'Image %s' % n)
    image = factory.LazyAttribute(
        lambda _: ContentFile(
            factory.django.ImageField()._make_data(
                {'width': 1024, 'height': 768}
            ), 'example.jpg'
        )
    )


class PlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Plant
        django_get_or_create = (
            'title', 'slug', 'description', 'category', 'shade', 'moisture', 'wind', 'soil', 'growth_rate')

    title = factory.sequence(lambda n: 'Title %s' % n)
    slug = factory.LazyAttribute(lambda o: o.title)
    description = factory.sequence(lambda n: 'Je suis une description : %s' % n)
    category = factory.SubFactory(CategoryFactory)

    shade = factory.sequence(lambda n: 'Plein ombre')
    moisture = factory.sequence(lambda n: 'Sol sec')
    wind = factory.sequence(lambda n: 'Exposition maritime')
    soil = factory.sequence(lambda n: 'Argile lourde')
    growth_rate = factory.sequence(lambda n: 'Vite')

    image = factory.SubFactory(ImageFactory)


class FavoritePlantFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FavoritePlant
        django_get_or_create = ('plant',)

    plant = factory.SubFactory(PlantFactory)
