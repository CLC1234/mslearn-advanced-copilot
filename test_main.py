from main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200


def test_countries():
    response = client.get("/countries")
    assert response.status_code == 200
    assert sorted(response.json()) == ["England", "France", "Germany", "Italy", "Peru", "Portugal", "Spain"]
    def test_get_cities_spain():
        response = client.get("/countries/Spain/cities")
        assert response.status_code == 200
        # The expected cities depend on the contents of weather.json.
        # If you know the expected list, replace the next line accordingly.
        assert isinstance(response.json(), list)
        assert len(response.json()) > 0  # Spain should have at least one city