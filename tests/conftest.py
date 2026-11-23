import os
import pytest

# Ensure test environment settings
os.environ["DATABASE_URL"] = "sqlite:///:memory:"
os.environ["SECRET_KEY"] = "test-secret-key-that-is-long-enough-for-testing"


class FixedRng:
    """Stands in for random.Random so the computer's picks are predictable in tests."""

    def __init__(self, index=0, roll=0.99):
        self.index = index
        self.roll = roll

    def random(self):
        return self.roll

    def randrange(self, n):
        return self.index % n


@pytest.fixture
def app():
    from app import create_app
    from app.extensions import db

    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "test-secret-key",
        }
    )

    with test_app.app_context():
        db.create_all()
        yield test_app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
