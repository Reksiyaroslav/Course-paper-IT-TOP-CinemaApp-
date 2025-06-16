import pytest
from  litestar.testing import TestClient
from litestar.status_codes import HTTP_200_OK,HTTP_404_NOT_FOUND,HTTP_201_CREATED,HTTP_409_CONFLICT
from app.run import app  
from app.model.model_user import UserCreateRequest,UserUpdateRequest
import uuid
#Работую но нужно перезапускать какждый раз проблема не решена .
@pytest.fixture(scope="function")
def client():
     with  TestClient(app=app) as client:
        yield client


def test_create_user(client):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    data_user = UserCreateRequest(username = unique_username,password="sercretpassword",email=f"{unique_username}@example.com")
    response =   client.post("/user", json=data_user.dict())
    assert response.status_code == HTTP_201_CREATED
    data = response.json()
    print("Response status:", response.status_code)
    print("Response body:", response.json())
    # Попытка создать дубликат
    response2 =   client.post("/user", json=data_user.dict())
    assert response2.status_code == HTTP_409_CONFLICT

    assert data["username"] == unique_username
    assert "id" in data

def test_list_user(client):
    rensponse =  client.get("/user")
    assert  rensponse.status_code ==HTTP_200_OK
    data = rensponse.json()
    assert isinstance(data, list)
def test_id_user(client):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    data_user = UserCreateRequest(username = unique_username,password="sercretpassword",email=f"{unique_username}@example.com")
    create_response =  client.post("/user", json=data_user.dict())
    user_id = create_response.json()["id"]
    rensponse =  client.get(f"/user/id/{user_id}")
    assert  rensponse.status_code ==HTTP_200_OK
    data = rensponse.json()
    assert data["id"] == user_id
    response_not_found =  client.get(f"/user/id/{uuid.uuid4()}")
    assert response_not_found.status_code == HTTP_404_NOT_FOUND
def test_username_user(client):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    data_user = UserCreateRequest(username = unique_username,password="sercretpassword",email=f"{unique_username}@example.com")
    create_response =   client.post("/user", json=data_user.dict())
    create_response =  client.get(f"/user/name/{unique_username}")
    assert  create_response.status_code ==HTTP_200_OK
    data = create_response.json()
    assert data["username"] == unique_username
    response_not_found =  client.get(f"/user/name/lox")
    assert response_not_found.status_code == HTTP_404_NOT_FOUND
def test_username_and_password(client):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    password = "sercretpassword"
    data_user = UserCreateRequest(username = unique_username,password=password,email=f"{unique_username}@example.com")
    create_response =   client.post("/user", json=data_user.dict())
    create_response =  client.get(f"/user/name/{unique_username}/password/{password}")
    assert  create_response.status_code ==HTTP_200_OK
    data = create_response.json()
    assert data["username"] == unique_username
    response_not_found =  client.get(f"/user/name/{unique_username}/password/wrongpassword")
    assert response_not_found.status_code == HTTP_404_NOT_FOUND
def test_update_user(client):
    unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
    data_user = UserCreateRequest(username=unique_username,email=f"{unique_username}@example.com", password= "securepassword")
    create_resp =  client.post("/user", json=data_user.dict())
    user_id = create_resp.json()["id"]

    update_data = UserUpdateRequest( email= f"updated_{unique_username}@example.com",
        password ="newpassword")
    response =  client.put(f"/user/id/{user_id}", json=update_data.dict())
    assert response.status_code == HTTP_200_OK
    data = response.json()
    assert data["email"] == update_data["email"]

    response_not_found =  client.put(f"/user/id/{uuid.uuid4()}", json=update_data.dict())
    assert response_not_found.status_code == HTTP_404_NOT_FOUND