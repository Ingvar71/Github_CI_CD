import factory.alchemy
import factory.fuzzy as fuzzy
import random

from hw_29.srk.app import db
from hw_29.srk.models import Client, Parking


class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session

    name = factory.Faker("first_name")
    surname = factory.Faker("last_name")
    credit_cart = factory.LazyAttribute(
        lambda x: random.choice([str(factory.Faker("credit_card_number")), None])
    )
    car_number = fuzzy.FuzzyText(length=8, chars="1234567890ABCDEFGHIJKLMNOPQR")


class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker("address")
    opened = factory.Faker("boolean")
    count_place = random.randint(90, 120)
    count_available_places = factory.LazyAttribute(lambda x: random.randint(40, 70))
