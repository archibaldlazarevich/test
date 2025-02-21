from .factories import ParkingFactory, ClientFactory
from ..src.models import Parking, Client

def test_create_client(app, db):
    _client = ClientFactory()
    db.session.commit()
    assert _client.id is not None
    assert len(db.session.query(Client).all()) == 1

def test_create_parking(app, db):
    parking = ParkingFactory()
    db.session.commit()
    assert parking.id is not None
    assert len(db.session.query(Parking).all()) == 1
