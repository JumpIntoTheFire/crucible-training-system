"""Tests for /workouts endpoints (JWT protected)."""

REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"
WORKOUTS_URL = "/workouts"

_USER_A = {"username": "workout_user_a", "email": "ua@example.com", "password": "SecurePass123"}
_USER_B = {"username": "workout_user_b", "email": "ub@example.com", "password": "SecurePass123"}

SAMPLE_PLAN = {
    "name": "Push Day",
    "exercises": [
        {
            "sets": 4,
            "reps": 8,
            "rest": 90,
            "exercise": {
                "id": 1,
                "name": "Bench Press",
                "category": "strength",
                "level": "intermediate",
                "primaryMuscles": ["chest"],
                "startImage": "/images/bench/0.jpg",
            },
        }
    ],
}


def _register_and_login(client, user):
    client.post(REGISTER_URL, json=user)
    res = client.post(LOGIN_URL, data={"username": user["username"], "password": user["password"]})
    return res.json()["access_token"]


def auth_header(token):
    return {"Authorization": f"Bearer {token}"}


# ── Unauthenticated access ────────────────────────────────────────────────────

def test_list_workouts_requires_auth(client):
    res = client.get(WORKOUTS_URL)
    assert res.status_code == 401


def test_create_workout_requires_auth(client):
    res = client.post(WORKOUTS_URL, json=SAMPLE_PLAN)
    assert res.status_code == 401


# ── Authenticated CRUD ────────────────────────────────────────────────────────

def test_create_and_list_workout(client):
    token = _register_and_login(client, _USER_A)
    res = client.post(WORKOUTS_URL, json=SAMPLE_PLAN, headers=auth_header(token))
    assert res.status_code == 201
    body = res.json()
    assert body["name"] == "Push Day"
    assert len(body["exercises"]) == 1

    list_res = client.get(WORKOUTS_URL, headers=auth_header(token))
    assert list_res.status_code == 200
    assert any(p["name"] == "Push Day" for p in list_res.json())


def test_delete_workout(client):
    token = _register_and_login(client, {"username": "del_user", "email": "del@example.com", "password": "SecurePass123"})
    plan = client.post(WORKOUTS_URL, json=SAMPLE_PLAN, headers=auth_header(token)).json()

    del_res = client.delete(f"{WORKOUTS_URL}/{plan['id']}", headers=auth_header(token))
    assert del_res.status_code == 204

    list_res = client.get(WORKOUTS_URL, headers=auth_header(token))
    assert not any(p["id"] == plan["id"] for p in list_res.json())


def test_cannot_delete_other_users_workout(client):
    token_a = _register_and_login(client, _USER_B)
    token_b = _register_and_login(client, {"username": "other_user", "email": "other@example.com", "password": "SecurePass123"})

    plan = client.post(WORKOUTS_URL, json=SAMPLE_PLAN, headers=auth_header(token_a)).json()
    res = client.delete(f"{WORKOUTS_URL}/{plan['id']}", headers=auth_header(token_b))
    assert res.status_code == 404


def test_workout_entry_validation(client):
    token = _register_and_login(client, {"username": "val_user", "email": "val@example.com", "password": "SecurePass123"})

    # Sets out of range
    bad_plan = {**SAMPLE_PLAN, "exercises": [{**SAMPLE_PLAN["exercises"][0], "sets": 0}]}
    res = client.post(WORKOUTS_URL, json=bad_plan, headers=auth_header(token))
    assert res.status_code == 422

    # Rest out of range
    bad_plan2 = {**SAMPLE_PLAN, "exercises": [{**SAMPLE_PLAN["exercises"][0], "rest": 9999}]}
    res2 = client.post(WORKOUTS_URL, json=bad_plan2, headers=auth_header(token))
    assert res2.status_code == 422
