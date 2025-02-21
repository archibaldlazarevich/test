from datetime import datetime
from typing import List

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import DefaultMeta

db: SQLAlchemy = SQLAlchemy()


class BaseModel(db.Model, metaclass=DefaultMeta):  # type: ignore
    __abstract__ = True


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///prod.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    from .models import Client, ClientParking, Parking

    def create_db():
        db.create_all()

    with app.app_context():
        create_db()

    @app.route("/clients", methods=["GET"])
    def get_client_list():
        """Метод описывающий работу эндпоинта
        для получения списка всех клиентов в базе данных"""
        clients: List[Client] = db.session.query(Client).all()
        user_list: list = [c.to_json() for c in clients]
        return jsonify(user_list), 200

    @app.route("/clients/<client_id>", methods=["GET"])
    def get_client_ifo_by_id(client_id: int):
        """Метод описывающий работу эндпоинта
        для получения информации о клиенте по его id"""
        client: Client | None = db.session.get(Client, client_id)
        if client is None:
            return f"Ошибка, клиента с id {client_id} нет в базе данных", 404
        return jsonify(client.to_json()), 200

    @app.route("/clients", methods=["POST"])
    def post_new_client():
        """Метод описывающий работу эндпоинта
        для добавления нового пользователя в базу данных"""

        name = request.form.get("name")
        surname = request.form.get("surname")
        credit_card = request.form.get("credit_card")
        car_number = request.form.get("car_number")

        new_client = Client(
            name=name,
            surname=surname,
            credit_card=credit_card,
            car_number=car_number,
        )
        db.session.add(new_client)
        db.session.commit()
        return f"Новый пользователь {surname} {name} добавлен успешно.", 201

    @app.route("/parkings", methods=["POST"])
    def post_new_parking():
        """Метод описывающий работу эндпоинта
        для добавления нового паркинга в бд"""
        address = request.form.get("address")
        opened = bool(request.form.get("opened"))
        count_places = request.form.get("count_places")
        count_available_places = request.form.get("count_available_places")

        new_parking = Parking(
            address=address,
            opened=opened,
            count_places=count_places,
            count_available_places=count_available_places,
        )
        db.session.add(new_parking)
        db.session.commit()
        return f"Новый паркинг по адресу {address} добавлен", 201

    @app.route("/client_parkings", methods=["POST"])
    def post_new_client_parking():
        """Метод описывающий работу эндпоинта
        по добавлению клиента, пользующегося паркингом"""
        client_id = request.form.get("client_id")
        parking_id = request.form.get("parking_id")
        time_in = datetime.now()
        check_parking: Parking = db.session.get(Parking, parking_id)
        if check_parking.opened and check_parking.count_available_places != 0:
            check_parking.count_available_places -= 1
            new_client_parking: ClientParking = ClientParking(
                client_id=client_id, parking_id=parking_id, time_in=time_in
            )
            db.session.add(new_client_parking)
            db.session.commit()
            return (
                f"Клиент с id {client_id} въехал на парковку {parking_id} "
                f"в {time_in.strftime('%H:%M:%S')}"
            ), 201
        return (
            "Данная парковка занята, " "клиент не смог припарковаться"
        ), 404

    @app.route("/client_parkings", methods=["DELETE"])
    def delete_client_parking():
        """Метод описывающий работы эндпоинта
        по присваиванию клиенту времени выезда с парковки"""
        client_id = request.form.get("client_id")
        parking_id = request.form.get("parking_id")
        time_out = datetime.now()

        check_client: Client = db.session.get(Client, client_id)
        if check_client.credit_card is None:
            return ("У клиента не привязана" " карта для оплаты"), 404

        check_client_parking: ClientParking = db.session.get(
            ClientParking, client_id
        )
        if check_client_parking.time_in > time_out:
            return ("Время выезда клиента меньше," " чем время заезда"), 404
        check_client_parking.time_out = time_out

        check_parking: Parking = db.session.get(Parking, parking_id)
        check_parking.count_available_places += 1
        db.session.commit()

        return (
            f"Клиент {client_id} покинул парковку "
            f"{parking_id} в {time_out.strftime('%H:%M:%S')}",
            202,
        )

    return app
