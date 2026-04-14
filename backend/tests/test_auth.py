"""Tests for /auth/register and /auth/login endpoints."""
import pytest


REGISTER_URL = "/auth/register"
LOGIN_URL = "/auth/login"

VALID_USER = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "SecurePass123",
}


# ── Register ──────────────────────────────────────────────────────────────────

def test_register_success(client):
    res = client.post(REGISTER_URL, json=VALID_USER)
    assert res.status_code == 201
    body = res.json()
    assert "access_token" in body
    assert body["username"] == VALID_USER["username"]
    assert body["token_type"] == "bearer"


def test_register_duplicate_username(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(REGISTER_URL, json=VALID_USER)
    assert res.status_code == 409
    assert "already registered" in res.json()["detail"]


def test_register_weak_password(client):
    res = client.post(REGISTER_URL, json={**VALID_USER, "username": "other", "email": "other@example.com", "password": "short"})
    assert res.status_code == 422


def test_register_invalid_email(client):
    res = client.post(REGISTER_URL, json={**VALID_USER, "username": "other2", "email": "not-an-email"})
    assert res.status_code == 422


def test_register_short_username(client):
    res = client.post(REGISTER_URL, json={**VALID_USER, "username": "ab", "email": "ab@example.com"})
    assert res.status_code == 422


# ── Login ─────────────────────────────────────────────────────────────────────

def test_login_success(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(LOGIN_URL, data={"username": VALID_USER["username"], "password": VALID_USER["password"]})
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert body["username"] == VALID_USER["username"]


def test_login_with_email(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(LOGIN_URL, data={"username": VALID_USER["email"], "password": VALID_USER["password"]})
    assert res.status_code == 200


def test_login_wrong_password(client):
    client.post(REGISTER_URL, json=VALID_USER)
    res = client.post(LOGIN_URL, data={"username": VALID_USER["username"], "password": "WrongPassword"})
    assert res.status_code == 401


def test_login_unknown_user(client):
    res = client.post(LOGIN_URL, data={"username": "nobody", "password": "irrelevant"})
    assert res.status_code == 401
