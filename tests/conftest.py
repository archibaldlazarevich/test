import pytest
from src.app import create_app, db as _db
from src.models import Client, Parking, ClientParking
from datetime import datetime


@pytest.fixture
def app():
    _app = create_app()
    _app.config["TESTING"] = True
    _app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    with _app.app_context():
        _db.create_all()
        _client_1 = Client(id=1,
                        name="name",
                        surname="surname",
                        credit_card= 'credit_card',
                        car_number= 'car_number')
        _client_2 = Client(id=2,
                           name="names",
                           surname="surnames",
                           credit_card='credit_cards',
                           car_number='car_numbers')
        parking= Parking(id= 1,
                         address= 'address',
                         opened = True,
                         count_places = 125,
                         count_available_places = 10)
        client_parking = ClientParking(id = 1,
                                       client_id= 1,
                                       parking_id = 1,
                                       time_in = datetime.now())
        _db.session.add_all([_client_1, _client_2])
        _db.session.add(parking)
        _db.session.add(client_parking)

        yield _app

        _db.session.close()
        _db.drop_all()

@pytest.fixture
def client(app):
    client = app.test_client()
    yield client


@pytest.fixture
def db(app):
    with app.app_context():
        yield _db