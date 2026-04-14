"""Tests for GET /exercises endpoint."""


def test_exercises_returns_list(client):
    res = client.get("/exercises")
    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_exercises_pagination_defaults(client):
    res = client.get("/exercises")
    assert res.status_code == 200
    assert len(res.json()) <= 20


def test_exercises_custom_limit(client):
    res = client.get("/exercises?limit=5")
    assert res.status_code == 200
    assert len(res.json()) <= 5


def test_exercises_limit_too_large(client):
    res = client.get("/exercises?limit=999")
    assert res.status_code == 422


def test_exercises_skip_negative(client):
    res = client.get("/exercises?skip=-1")
    assert res.status_code == 422


def test_exercises_invalid_muscle(client):
    res = client.get("/exercises?muscle=notamuscle")
    assert res.status_code == 400


def test_exercises_valid_muscle(client):
    res = client.get("/exercises?muscle=chest")
    assert res.status_code == 200


def test_exercises_invalid_category(client):
    res = client.get("/exercises?category=yoga")
    assert res.status_code == 400


def test_exercises_valid_category(client):
    res = client.get("/exercises?category=strength")
    assert res.status_code == 200


def test_exercises_search(client):
    res = client.get("/exercises?search=bench")
    assert res.status_code == 200
    for ex in res.json():
        assert "bench" in ex["name"].lower()
