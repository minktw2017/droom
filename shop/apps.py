from django.apps import AppConfig
from suit.apps import DjangoSuitConfig


class ShopConfig(AppConfig):
    name = 'shop'


class SuitConfig(DjangoSuitConfig):
    layout = 'vertical'
