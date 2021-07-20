import factory
from django.core.files.base import ContentFile

from plant.models import Plant, Category, ImagePlant


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
        django_get_or_create = ('title', 'slug', 'description', 'category')

    title = factory.sequence(lambda n: 'Title %s' % n)
    slug = factory.LazyAttribute(lambda o: o.title)
    description = factory.sequence(lambda n: 'Je suis une description : %s' % n)
    category = factory.SubFactory(CategoryFactory)
    image = factory.SubFactory(ImageFactory)
