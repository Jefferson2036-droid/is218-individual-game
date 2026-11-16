import os

# Must be set before the app is imported: tests use a throwaway in-memory database.
os.environ["DATABASE_URL"] = "sqlite://"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-hs256-0123456789"


class FixedRng:
    """Stands in for random.Random so the computer's picks are predictable in tests."""

    def __init__(self, index=0, roll=0.99):
        self.index = index   # which fighter a "random" pick returns (0 knight, 1 archer, 2 wizard)
        self.roll = roll     # value of random(); 0.99 means "never try to predict"

    def random(self):
        return self.roll

    def randrange(self, n):
        return self.index % n


import pytest  # noqa: E402


@pytest.fixture
def client():
    """A test client with an empty database and a computer that always sends Knight."""
    pytest.importorskip("fastapi")
    pytest.importorskip("sqlalchemy")
    pytest.importorskip("httpx")
    from fastapi.testclient import TestClient

    from app.db import Base, engine
    from app.deps import get_rng
    from app.main import app

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    app.dependency_overrides[get_rng] = lambda: FixedRng(index=0)
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
