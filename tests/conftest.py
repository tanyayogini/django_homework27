from pytest_factoryboy import register

from tests.factories import UserFactory, AdFactory

pytest_plugins = "tests.fixtures"

register(UserFactory)
register(AdFactory)
