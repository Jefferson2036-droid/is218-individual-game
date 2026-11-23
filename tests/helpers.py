"""Helper functions for Flask tests."""


def sign_up(client, username="jeff", password="password123"):
    return client.post(
        "/sign-up",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def sign_in(client, username="jeff", password="password123"):
    return client.post(
        "/sign-in",
        data={"username": username, "password": password},
        follow_redirects=True,
    )


def sign_out(client):
    return client.post("/sign-out", follow_redirects=True)
