import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.models import Base, get_db
from backend.main import app

# Tests must use a separate database. The session-scoped `create_tables`
# fixture below runs `Base.metadata.drop_all()` on teardown — pointing it at a
# shared DB wipes everything (this happened on 2026-05-04: pytest in the
# backend container picked up `DATABASE_URL=cts_db` and dropped the live
# tables, taking 873 ingested exercises with it).
#
# The fix:
#   - Read TEST_DATABASE_URL (NOT DATABASE_URL).
#   - If TEST_DATABASE_URL is unset AND DATABASE_URL is set, refuse to run
#     rather than fall back to the production URL. The operator has to
#     opt-in to a test DB explicitly.
#   - If neither is set, default to a local cts_test DB (covers
#     `pytest` run from the host with no Docker, no env). Anyone hitting
#     the default has clearly never used the production stack.
DATABASE_URL = os.environ.get("DATABASE_URL")
TEST_DATABASE_URL = os.environ.get("TEST_DATABASE_URL")

if not TEST_DATABASE_URL:
    if DATABASE_URL:
        raise RuntimeError(
            "TEST_DATABASE_URL is required when DATABASE_URL is set. "
            "Tests run drop_all() on teardown — falling back to DATABASE_URL "
            "would wipe the shared/production database. "
            "Set TEST_DATABASE_URL to a dedicated test database "
            "(e.g. postgresql://postgres:postgres@db:5432/cts_test) before running pytest."
        )
    TEST_DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/cts_test"

if DATABASE_URL and TEST_DATABASE_URL == DATABASE_URL:
    raise RuntimeError(
        f"TEST_DATABASE_URL must differ from DATABASE_URL "
        f"(both currently point at {TEST_DATABASE_URL!r}). "
        f"Tests run drop_all() on teardown."
    )

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="session", autouse=True)
def create_tables():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
