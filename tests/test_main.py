import json
from re import findall

from fastapi.testclient import TestClient

from ..main import app

client = TestClient(app)

CORRECT_URL = json.dumps({"url": "https://google.com"})
ANOTHER_CORRECT_URL = json.dumps({"url": "https://google.com/hello"})
INVALID_URL = json.dumps({"url": "https://google"})


def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Available Endpoints: /encode, /decode",
    }


def test_nonexistent_endpoint():
    response = client.post("/encode_decode", CORRECT_URL)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found",
    }


def test_method_not_allowed():
    response = client.get("/encode")
    assert response.status_code == 405
    assert response.json() == {
        "detail": "Method Not Allowed",
    }


def test_encode_correct_url():
    response = client.post("/encode", CORRECT_URL)
    assert response.status_code == 200
    url_from_correct_url = json.loads(CORRECT_URL)["url"]
    assert response.json()['long_url'] == url_from_correct_url
    short_url_key = findall(
        r"((?<=http://short.est/)[a-zA-Z0-9]{6})$",
        response.json()['short_url']
    )
    assert len(short_url_key) == 1


def test_encode_correct_url_twice():
    response_1 = client.post("/encode", CORRECT_URL)
    response_2 = client.post("/encode", CORRECT_URL)

    assert response_1.status_code == 200
    url_from_correct_url = json.loads(CORRECT_URL)["url"]
    assert response_1.json()['long_url'] == url_from_correct_url
    short_url_key = findall(
        r"((?<=http://short.est/)[a-zA-Z0-9]{6})$",
        response_1.json()['short_url']
    )
    assert len(short_url_key) == 1
    assert response_1.json() == response_2.json()


def test_encode_nothing():
    response = client.post("/encode")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "No URL Passed",
    }


def test_encode_invalid_url():
    response = client.post("/encode", INVALID_URL)
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Invalid URL",
    }


def test_decode_correct_url():
    response_encode = client.post("/encode", CORRECT_URL)
    encoded_json = response_encode.json()
    json_for_decoding = json.dumps({"url": encoded_json["short_url"]})
    response_decode = client.post("/decode", json_for_decoding)

    assert response_decode.status_code == 200
    assert response_decode.json() == encoded_json


def test_decode_correct_url_twice():
    response_encode = client.post("/encode", CORRECT_URL)
    encoded_json = response_encode.json()
    json_for_decoding = json.dumps({"url": encoded_json["short_url"]})
    response_1 = client.post("/decode", json_for_decoding)
    response_2 = client.post("/decode", json_for_decoding)

    assert response_1.status_code == response_2.status_code == 200
    assert response_1.json() == response_2.json() == encoded_json


def test_decode_nothing():
    response = client.post("/decode")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "No URL Passed",
    }


def test_decode_nonexistent_url():
    response = client.post("/decode", ANOTHER_CORRECT_URL)
    assert response.status_code == 404
    assert response.json() == {
        "detail": "URL Not Found",
    }


def test_decode_invalid_url():
    response = client.post("/decode", INVALID_URL)
    assert response.status_code == 422
    assert response.json() == {
        "detail": "Invalid URL",
    }
