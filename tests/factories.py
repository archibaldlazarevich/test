import factory
import random


from src.app import db
from src.models import Client, Parking

class ClientFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Client
        sqlalchemy_session = db.session
    name = factory.Faker('first_name')
    surname = factory.Faker('last_name')
    credit_card = factory.LazyFunction(lambda : random.choice([None, 'credit_card_number']))
    car_number = factory.Faker('port_number')

class ParkingFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Parking
        sqlalchemy_session = db.session

    address = factory.Faker('address')
    opened = factory.LazyFunction(lambda: random.choice([True, False]))
    count_places = factory.LazyFunction(lambda : random.randint(150, 1584))
    count_available_places = factory.LazyAttribute(lambda x: random.randint(0, 15))
