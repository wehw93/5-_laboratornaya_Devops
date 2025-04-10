from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)

# Существующие пользователи
users = [
    {
        'id': 1,
        'name': 'Ivan Ivanov',
        'email': 'i.i.ivanov@mail.com',
    },
    {
        'id': 2,
        'name': 'Petr Petrov',
        'email': 'p.p.petrov@mail.com',
    }
]

def test_get_existed_user():
    '''Получение существующего пользователя'''
    response = client.get("/api/v1/user", params={'email': users[0]['email']})
    assert response.status_code == 200
    assert response.json() == users[0]

def test_get_unexisted_user():
    '''Получение несуществующего пользователя'''
    response = client.get("/api/v1/user", params={'email': 'noname@mail.ru'})
    assert response.status_code == 404

def test_create_user_with_valid_email():
    '''Создание пользователя с уникальной почтой'''
    user = {
        'name': 'Egor Titov',
        'email': 'titov@mail.ru',
    }
    response = client.post("/api/v1/user", json=user)
    assert response.status_code == 201
    assert 'id' in response.json()


def test_create_user_with_invalid_email():
    '''Создание пользователя с почтой, которую использует другой пользователь'''
    user = {
        'name': 'Titov Daniel',
        'email': users[0]['email'],
    }
    response = client.post("/api/v1/user", json=user)
    assert response.status_code == 409  
    assert response.json()['detail'] == 'Email already in use'

def test_delete_user():
    '''Удаление пользователя'''
    user_to_delete = users[0] 
    response = client.delete(f"/api/v1/user?email={user_to_delete['email']}")
    assert response.status_code == 200  