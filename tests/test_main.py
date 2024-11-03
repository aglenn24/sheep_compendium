#Import TestClient to simulate API requests
from fastapi.testclient import TestClient

# Import the FastAPI app instance form the controller module
from main import app

# Create a TestClient instance for the FastAPI app
client = TestClient(app)

# Define a test function for reading a specific sheep
def test_read_sheep():
    # Send a GET request to the endpoint "/sheep/1"
    response = client.get("/sheep/1")

    # Assert that the response status code is 200 (OK)
    assert response.status_code == 200

    # Assert that the resonse JSON matches the expected data
    assert response.json() == {
        # Expected JSON structure
        "id": 1,
        "name": "Spice",
        "breed": "Gotland",
        "sex": "ewe"
    }

def test_add_sheep():
    # Prepare the new sheep data in a dictionary format
    new_sheep = {"id": 8, "name": "Kewtee", "breed": "Babydoll", "sex": "ewe"}

    # Send a POST request to the endpoint
    response = client.post("/sheep/", json=new_sheep)

    # Assert that the response status code is 201
    assert response.status_code == 201

    # Assert that the response JSON matches the new sheep data
    assert response.json() == new_sheep

    # Verify that the sheep was added to database
    response = client.get("/sheep/8")
    assert response.status_code == 200

def test_update_sheep():
    new_sheep = {"id": 1, "name": "Kewtee", "breed": "Babydoll"}
    response = client.put("/sheep/", json=new_sheep)
    assert response.status_code == 200
    assert response.json() == new_sheep
    response = client.get("/sheep/1")
    assert response.status_code == 200

def test_delete_sheep():
    response = client.delete("/sheep/1")
    assert response.status_code == 204
    response = client.get("/sheep/1")
    assert response.status_code == 404