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
