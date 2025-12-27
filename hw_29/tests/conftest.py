import pytest

from ..srk.app import create_app
from ..srk.app import db as _db
from ..srk.models import Client, Parking


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()

        client = Client(
            id=1,
            name="Nick",
            surname="Nolton",
            credit_cart="2569456812398954",
            car_number="HJK125U52",
        )
        parking = Parking(
            id=1,
            address="1 GYPSY LN RAYMOND NH 03077-1412 USA",
            opened=True,
            count_place=60,
            count_available_places=37,
        )

        _db.session.add(client)
        _db.session.add(parking)
        _db.session.commit()

        yield _app
        _db.session.close()
        _db.drop_all()


@pytest.fixture()
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture()
def db(app):
    with app.app_context():
        yield _db
