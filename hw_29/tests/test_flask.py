import json
import pytest
from ..srk.models import Client, Parking, ClientParking
import time
from datetime import datetime


def test_client(client) -> None:
    resp = client.get("/clients/1")
    assert resp.status_code == 200
    assert resp.json == {"id": 1, "name": "Nick", "surname": "Nolton", "credit_cart": "2569456812398954",
                         "car_number": "HJK125U52"}


def test_create_client(client) -> None:
    client_data = {"id": 2, "name": "Jonathan", "surname": "Nielsen", "credit_cart": "5863426859631245",
                         "car_number": "4JKR8UH52"}
    resp = client.post("/clients", data=client_data)

    assert resp.status_code == 201


def test_create_parking(client) -> None:
    parking_data = {"id": 2, "address": "2 HOBBS ST CONWAY NH 03818-6251 USA", "opened": True,
                    "count_place": 85, "count_available_places": 51}
    resp = client.post("/parkings", data=parking_data)

    assert resp.status_code == 201


@pytest.mark.parametrize("route", ["/clients/1", "/clients", "/"])
def test_route_status(client, route):
    rv = client.get(route)
    assert rv.status_code == 200


@pytest.mark.parking
def test_client_parking_in(client, db) -> None:
    client_parking_data = {"id": 1, "client_id": 1, "parking_id": 1}
    parking_in = db.session.get(Parking, 1)
    before = parking_in.count_available_places
    status = parking_in.opened
    resp = client.post('/client_parkings', data=client_parking_data)
    after = parking_in.count_available_places
    assert after < before
    assert resp.status_code == 201
    assert status == True


@pytest.mark.parking
def test_client_parking_out(client, db) -> None:
    client_parking_data = {"id": 1, "client_id": 1, "parking_id": 1}
    client_out = db.session.get(Client, 1)
    parking_out = db.session.get(Parking, 1)
    after = parking_out.count_available_places
    resp = client.post('/client_parkings', data=client_parking_data)
    before = parking_out.count_available_places
    entrance_parking = db.session.get(ClientParking, 1)
    time_parking = entrance_parking.time_on
    time.sleep(5)
    exit_parking = datetime.now()
    resp = client.delete('/client_parkings', data=client_parking_data)
    assert after > before
    assert True
    assert client_out.credit_cart is not None
    assert exit_parking > time_parking


