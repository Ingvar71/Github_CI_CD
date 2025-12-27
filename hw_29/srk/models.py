from typing import Any, Dict

from .app import db


class Client(db.Model):  # type: ignore
    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    name = db.Column(db.String(50), nullable=False)  # type: ignore
    surname = db.Column(db.String(50), nullable=False)  # type: ignore
    credit_cart = db.Column(db.String(50), nullable=True)  # type: ignore
    car_number = db.Column(db.String(10), nullable=True)  # type: ignore

    id_client = db.relationship(  # type: ignore
        "ClientParking", back_populates="client"  # type: ignore
    )

    def __repr__(self):
        return f"Client {self.name} {self.surname}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Parking(db.Model):  # type: ignore
    __tablename__ = "parking"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    address = db.Column(db.String(100), nullable=False)  # type: ignore
    opened = db.Column(db.Boolean, nullable=True)  # type: ignore
    count_place = db.Column(db.Integer, nullable=False)  # type: ignore
    count_available_places = db.Column(  # type: ignore
        db.Integer, nullable=False  # type: ignore
    )

    id_parking = db.relationship(  # type: ignore
        "ClientParking", back_populates="parking"  # type: ignore
    )

    def __repr__(self):
        return f"Parking {self.address} {self.opened}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class ClientParking(db.Model):  # type: ignore
    __tablename__ = "client_parking"

    id = db.Column(db.Integer, primary_key=True)  # type: ignore
    client_id = db.Column(  # type: ignore
        db.Integer,  # type: ignore
        db.ForeignKey("client.id"),  # type: ignore
        nullable=False,  # type: ignore
        unique=True,  # type: ignore
    )
    parking_id = db.Column(  # type: ignore
        db.Integer,  # type: ignore
        db.ForeignKey("parking.id"),  # type: ignore
        nullable=False,  # type: ignore
        unique=True,  # type: ignore
    )
    time_on = db.Column(db.DateTime, nullable=True)  # type: ignore
    time_out = db.Column(db.DateTime, nullable=True)  # type: ignore

    client = db.relationship(  # type: ignore
        "Client", back_populates="id_client"  # type: ignore
    )
    parking = db.relationship(  # type: ignore
        "Parking", back_populates="id_parking"  # type: ignore
    )

    def __repr__(self):
        return f"Client_Parking {self.client_id} {self.parking_id}"

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
