import pytest
import json

@pytest.mark.parametrize('route', ['clients', 'clients/1'])
def test_route_status(client, route) -> None:
    rv = client.get(route)
    assert rv.status_code == 200

def test_create_client(client) -> None:
    client_data = {'name': 'Nik', 'surname': 'ivanov', 'credit_card': 'qwrqwr', 'car_number': '7894'}
    resp = client.post('/clients', data= client_data)
    assert resp.status_code == 201

def test_create_parking(client) -> None:
    parking_data = {'address': 'address', 'opened': True, 'count_places' : '548', 'count_available_places': '5'}
    resp = client.post('/parkings', data= parking_data)
    assert resp.status_code == 201

@pytest.mark.parking
def test_new_parking_client(client) -> None:
    new_data = {'client_id': '2', 'parking_id': '1'}
    resp =client.post('/client_parkings', data=new_data)
    assert resp.status_code == 201

@pytest.mark.parking
def test_leave_parking(client) -> None:
    new_data = {'client_id': '1', 'parking_id': '1'}
    resp = client.delete('/client_parkings', data=new_data)
    assert resp.status_code == 202