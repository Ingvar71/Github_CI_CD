from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from typing import List
from datetime import datetime
import datetime


db = SQLAlchemy()

from .models import Client, Parking, ClientParking


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///car_parking.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    @app.before_request
    def before_request_func():
        db.create_all()

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        db.session.remove()

    @app.route("/", methods=["GET"])
    def get_template_handler():
        return "OK"

    @app.route("/clients", methods=["GET"])
    def get_clients_handler():
        """Getting a list of all clients"""
        clients: List[Client] = db.session.query(Client).all()
        clients_list = [c.to_json() for c in clients]
        return jsonify(clients_list), 200

    @app.route("/clients/<int:client_id>", methods=["GET"])
    def get_id_client_handler(client_id):
        """Getting clients information by id"""
        client: Client = db.session.query(Client).get(client_id)
        return jsonify(client.to_json()), 200

    @app.route("/clients", methods=["POST"])
    def create_client_handler():
        """
        Creating a new client
        """
        id = request.form.get("id", type=int)
        name = request.form.get("name", type=str)
        surname = request.form.get("surname", type=str)
        credit_cart = request.form.get("credit_cart", type=str)
        car_number = request.form.get("car_number", type=str)

        new_client = Client(
            id=id,
            name=name,
            surname=surname,
            credit_cart=credit_cart,
            car_number=car_number,
        )

        db.session.add(new_client)
        db.session.commit()
        return jsonify(new_client.to_json()), 201

    @app.route("/parkings", methods=["POST"])
    def create_parking_handler():
        """
        Creating a new parking
        """
        id = request.form.get("id", type=int)
        address = request.form.get("address", type=str)
        opened = request.form.get("opened", type=bool)
        count_place = request.form.get("count_place", type=int)
        count_available_places = request.form.get("count_available_places", type=int)

        new_parking = Parking(
            id=id,
            address=address,
            opened=opened,
            count_place=count_place,
            count_available_places=count_available_places,
        )

        db.session.add(new_parking)
        db.session.commit()
        return jsonify(new_parking.to_json()), 201

    @app.route("/client_parkings", methods=["POST"])
    def create_client_parking_handler():
        """
        entrance to parking
        """
        id = request.form.get("id", type=int)
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)

        parking: Parking = db.session.query(Parking).get(parking_id)
        if parking.opened == True:
            if parking.count_available_places > 0:
                current_date = datetime.datetime.now()
                new_parking = ClientParking(
                    id=id,
                    client_id=client_id,
                    parking_id=parking_id,
                    time_on=current_date,
                    time_out=None,
                )

                db.session.add(new_parking)

                count = parking.count_available_places
                if count:
                    parking.count_available_places = count - 1

                db.session.commit()

                return jsonify(parking.to_json()), 201
            else:
                return "No parking!", 200
        else:
            return "No parking!", 200

    @app.route("/client_parkings/", methods=["DELETE"])
    def delete_client_parking_handler():
        """
        entrance to parking
        """
        client_id = request.form.get("client_id", type=int)
        parking_id = request.form.get("parking_id", type=int)

        availability_credit_cart: Client = db.session.query(Client).get(client_id)
        if availability_credit_cart.credit_cart:
            date_of_return = datetime.datetime.now()

            i = (
                db.session.query(ClientParking)
                .filter(
                    ClientParking.client_id == client_id
                    and ClientParking.parking_id == parking_id
                )
                .first()
            )
            i.time_out = date_of_return
            db.session.commit()

            parking: Parking = db.session.query(Parking).get(parking_id)
            # count = parking.count_available_places
            # if count:
            #     parking.count_available_places = count + 1
            #     db.session.commit()

            if i:
                deleted_row_json = dict(
                    id=i.id,
                    client_id=i.client_id,
                    parking_id=i.parking_id,
                    time_on=i.time_on,
                    time_out=i.time_out,
                )
                db.session.delete(i)

                count = parking.count_available_places
                if count:
                    parking.count_available_places = count + 1

                db.session.commit()
                return jsonify(delete_row_attrs=deleted_row_json), 201

        else:
            return "No bank card!", 200

    return app
