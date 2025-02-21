from typing import Dict, Any
from datetime import datetime, UTC

from .app import db

class Client(db.Model):
    """Класс описывающий таблицу данных для клиента парковки"""
    __tablename__ = 'client'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable= False)
    surname = db.Column(db.String(50), nullable= False)
    credit_card = db.Column(db.String(50))
    car_number = db.Column(db.String(10))

    def __repr__(self):
        return (f'Клиент {self.surname} {self.name}, номер кредитной карты {self.credit_card},'
                f'номер автомобиля {self.car_number}')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

class Parking(db.Model):
    """Класс описывающий таблицу данных для всех доступных паркингов"""
    __tablname__ = 'parking'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(100), nullable=False)
    opened = db.Column(db.Boolean)
    count_places = db.Column(db.Integer, nullable=False)
    count_available_places  = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return (f'Паркинг, находится по адресу {self.address} {self.opened}, '
                f'количество мест {self.count_places}, '
                f'количество свободных мест {self.count_available_places}')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}

class ClientParking(db.Model):
    """Класс описывающий таблицу для всех клиентов, пользующимися парковками"""
    __tablename__ = 'client_parking'

    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'))
    parking_id = db.Column(db.Integer, db.ForeignKey('parking.id'))
    time_in = db.Column(db.DateTime)
    time_out = db.Column(db.DateTime)

    __table_args__ = (db.UniqueConstraint('client_id', 'parking_id', name='unique_client_parking'),)

    def __repr__(self):
        if self.time_out is None:
            return f'Клиент {self.client_id} припарковался в паркинге {self.parking_id} в {self.time_in}'
        else:
            return (f'Клиент {self.client_id} припарковался в паркинге {self.parking_id} в {self.time_in}'
                    f'а выехал в {self.time_out} ')

    def to_json(self) -> Dict[str, Any]:
        return {c.name: getattr(self, c.name) for c in
                self.__table__.columns}
