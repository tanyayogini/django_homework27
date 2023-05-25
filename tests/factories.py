import factory.django

from ads.models import Ad
from users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("name")
    password = "123"


class AdFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Ad

    name = 'test ad name'
    author = factory.SubFactory(UserFactory)
    price = 0
