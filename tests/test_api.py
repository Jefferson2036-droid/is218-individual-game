"""API tests. Need the web packages: pip install -r requirements-dev.txt"""

import pytest

from tests.helpers import ACCOUNT, play_match, register


# ---- pages ----

def test_home_page_and_script_are_served(client):
    home = client.get("/")
    assert home.status_code == 200
    assert "ARENA" in home.text and "/app.js" in home.text
    script = client.get("/app.js")
    assert script.status_code == 200 and "Arena Climb front end" in script.text


def test_unknown_api_paths_are_not_swallowed_by_the_pages(client):
    assert client.get("/api/nope").status_code == 404


# ---- accounts ----

def test_health(client):
    assert client.get("/api/health").json() == {"status": "ok"}


def test_register_creates_a_recruit_with_nothing(client):
    response = register(client)
    assert response.status_code == 201, response.text
    user = response.json()["user"]
    assert user["email"] == "player@example.com"          # stored lower-case
    assert user["display_name"] == "Jeff"
    assert (user["rank"], user["rank_name"], user["stars"], user["coins"], user["streak"]) == (0, "Recruit", 0, 0, 0)
    assert "password" not in str(response.json()).lower().replace("password_hash", "")
    assert response.json()["access_token"]


def test_duplicate_email_is_rejected_even_with_different_capitals(client):
    assert register(client).status_code == 201
    again = register(client, email="PLAYER@example.com")
    assert again.status_code == 409


@pytest.mark.parametrize(
    "changes",
    [{"email": "not-an-email"}, {"password": "short"}, {"display_name": ""}, {"display_name": "x" * 41}],
)
def test_invalid_registration_is_rejected(client, changes):
    assert register(client, **changes).status_code == 422


def test_me_requires_signing_in(client):
    assert client.get("/api/me").status_code == 401


def test_registering_signs_you_in_with_a_cookie(client):
    register(client)
    assert client.get("/api/me").json()["user"]["email"] == "player@example.com"


def test_login_logout_and_wrong_password(client):
    register(client)
    client.post("/api/auth/logout")
    client.cookies.clear()
    assert client.get("/api/me").status_code == 401

    assert client.post("/api/auth/login", json={"email": ACCOUNT["email"], "password": "wrong-password"}).status_code == 401
    assert client.post("/api/auth/login", json={"email": "nobody@example.com", "password": "whatever-123"}).status_code == 401

    ok = client.post("/api/auth/login", json={"email": "player@example.com", "password": ACCOUNT["password"]})
    assert ok.status_code == 200
    assert client.get("/api/me").status_code == 200


def test_bearer_token_works_without_cookies(client):
    token = register(client).json()["access_token"]
    client.cookies.clear()
    assert client.get("/api/me", headers={"Authorization": f"Bearer {token}"}).status_code == 200
    assert client.get("/api/me", headers={"Authorization": "Bearer nonsense"}).status_code == 401


# ---- matches ----

def test_matches_require_signing_in(client):
    assert client.post("/api/matches").status_code == 401


def test_a_round_is_decided_by_the_server(client):
    register(client)
    match_id = client.post("/api/matches").json()["match"]["id"]
    body = client.post(f"/api/matches/{match_id}/rounds", json={"pick": "wizard"}).json()
    assert body["round"] == {"pick": "wizard", "cpu": "knight", "result": "win", "predicted": None}
    assert (body["match"]["you"], body["match"]["cpu"], body["match"]["status"]) == (1, 0, "active")
    assert body["outcome"] is None


def test_invalid_pick_is_rejected(client):
    register(client)
    match_id = client.post("/api/matches").json()["match"]["id"]
    assert client.post(f"/api/matches/{match_id}/rounds", json={"pick": "dragon"}).status_code == 422


def test_winning_a_match_saves_the_result_and_rewards_the_player(client):
    register(client)
    match_id, body = play_match(client, "wizard")
    assert body["match"]["status"] == "won"
    assert body["outcome"]["won"] is True
    assert (body["outcome"]["stars_change"], body["outcome"]["coins_earned"]) == (1, 10)
    assert (body["user"]["stars"], body["user"]["coins"], body["user"]["streak"]) == (1, 10, 1)

    saved = client.get(f"/api/matches/{match_id}").json()["match"]
    assert (saved["status"], saved["you"], saved["cpu"], len(saved["rounds"])) == ("won", 3, 0, 3)
    assert client.get("/api/me").json()["user"]["stars"] == 1        # survives a fresh request


def test_losing_a_match_at_the_bottom_costs_nothing(client):
    register(client)
    _, body = play_match(client, "archer")
    assert body["match"]["status"] == "lost"
    assert body["outcome"]["won"] is False
    assert (body["user"]["stars"], body["user"]["coins"], body["user"]["streak"]) == (0, 0, 0)


def test_a_finished_match_cannot_be_played_again(client):
    register(client)
    match_id, _ = play_match(client, "wizard")
    assert client.post(f"/api/matches/{match_id}/rounds", json={"pick": "wizard"}).status_code == 409


def test_three_wins_rank_up_to_squire_and_unlock_gold_armor(client):
    register(client)
    body = None
    for _ in range(3):
        _, body = play_match(client, "wizard")
    assert body["outcome"]["ranked_up"] is True
    assert body["outcome"]["new_rank_name"] == "Squire"
    assert [item["id"] for item in body["outcome"]["unlocked_items"]] == ["gold-armor"]
    assert (body["user"]["rank"], body["user"]["stars"]) == (1, 0)
    assert body["user"]["coins"] == 3 * 10 + 25


def test_starting_a_new_match_abandons_the_unfinished_one(client):
    register(client)
    first = client.post("/api/matches").json()["match"]["id"]
    client.post(f"/api/matches/{first}/rounds", json={"pick": "wizard"})
    client.post("/api/matches")
    assert client.get(f"/api/matches/{first}").json()["match"]["status"] == "abandoned"
    assert client.post(f"/api/matches/{first}/rounds", json={"pick": "wizard"}).status_code == 409
    assert client.get("/api/me").json()["user"]["stars"] == 0        # abandoned matches change nothing


def test_players_cannot_see_or_play_each_others_matches(client):
    register(client)
    match_id = client.post("/api/matches").json()["match"]["id"]
    client.cookies.clear()
    register(client, email="other@example.com")
    assert client.get(f"/api/matches/{match_id}").status_code == 404
    assert client.post(f"/api/matches/{match_id}/rounds", json={"pick": "wizard"}).status_code == 404
