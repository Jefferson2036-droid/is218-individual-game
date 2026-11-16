"""Shared steps for the API tests."""

ACCOUNT = {"email": "Player@Example.com", "password": "hunter2-hunter2", "display_name": "Jeff"}


def register(client, **changes):
    return client.post("/api/auth/register", json={**ACCOUNT, **changes})


def play_match(client, pick):
    """Play one whole match with the same pick. Wizard wins, Archer loses (the computer sends Knight)."""
    match_id = client.post("/api/matches").json()["match"]["id"]
    body = None
    for _ in range(3):
        response = client.post(f"/api/matches/{match_id}/rounds", json={"pick": pick})
        assert response.status_code == 200, response.text
        body = response.json()
    return match_id, body


def reach_squire(client):
    """Three straight wins: Squire rank, Gold Armor unlocked, 55 coins."""
    for _ in range(3):
        play_match(client, "wizard")
