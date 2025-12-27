import random

import factory.alchemy
import factory.fuzzy as fuzzy

from hw_29.srk.app import db
from hw_29.srk.models import Client, Parking

password = "1234567890ABCDEFGHIJKLMNOPQR"
func = str(factory.Faker("credit_card_number")), None
func_lambd = random.randint(40, 70)


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_cart = factory.LazyAttribute(lambda x: random.choice(func))
    car_number = fuzzy.FuzzyText(length=8, chars=password)


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_place = random.randint(90, 120)
    count_available_places = factory.LazyAttribute(lambda x: func_lambd)
