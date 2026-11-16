"""Dashboard, account update and armory. Need the web packages: pip install -r requirements-dev.txt"""

from tests.helpers import ACCOUNT, play_match, reach_squire, register


def gear_item(body, item_id):
    return next(item for item in body["gear"]["items"] if item["id"] == item_id)


# ---- dashboard ----

def test_dashboard_requires_signing_in(client):
    assert client.get("/api/dashboard").status_code == 401


def test_new_player_dashboard_is_empty(client):
    register(client)
    body = client.get("/api/dashboard").json()
    assert body["user"]["rank_name"] == "Recruit"
    assert body["stats"] == {"matches_played": 0, "wins": 0, "losses": 0, "win_rate": None, "streak": 0}
    assert body["recent_matches"] == []
    assert len(body["gear"]["items"]) == 6
    assert not any(item["owned"] or item["equipped"] for item in body["gear"]["items"])
    assert body["gear"]["loadout"] == {"knight": None, "archer": None, "wizard": None}


def test_dashboard_shows_stats_and_history_newest_first(client):
    register(client)
    play_match(client, "wizard")     # win
    play_match(client, "archer")     # loss
    body = client.get("/api/dashboard").json()
    assert body["stats"] == {"matches_played": 2, "wins": 1, "losses": 1, "win_rate": 0.5, "streak": 0}
    history = body["recent_matches"]
    assert [row["won"] for row in history] == [False, True]
    assert (history[1]["you"], history[1]["cpu"], history[1]["stars_change"], history[1]["coins_earned"]) == (3, 0, 1, 10)
    assert history[0]["rank_name"] == "Recruit" and history[0]["finished_at"]


def test_unfinished_matches_are_not_in_the_dashboard(client):
    register(client)
    match_id = client.post("/api/matches").json()["match"]["id"]
    client.post(f"/api/matches/{match_id}/rounds", json={"pick": "wizard"})
    client.post("/api/matches")      # abandons the first
    body = client.get("/api/dashboard").json()
    assert body["stats"]["matches_played"] == 0 and body["recent_matches"] == []


def test_history_keeps_only_the_latest_ten(client):
    register(client)
    for _ in range(12):
        play_match(client, "archer")
    body = client.get("/api/dashboard").json()
    assert body["stats"]["matches_played"] == 12
    assert len(body["recent_matches"]) == 10


def test_dashboard_only_shows_my_own_matches(client):
    register(client)
    play_match(client, "wizard")
    client.cookies.clear()
    register(client, email="other@example.com")
    assert client.get("/api/dashboard").json()["stats"]["matches_played"] == 0


def test_ranking_up_shows_the_unlocked_gear(client):
    register(client)
    reach_squire(client)
    body = client.get("/api/dashboard").json()
    assert (body["user"]["rank_name"], body["user"]["coins"]) == ("Squire", 55)
    assert gear_item(body, "gold-armor")["owned"] is True
    assert gear_item(body, "flame-bow")["owned"] is False
    assert gear_item(body, "flame-bow")["unlock_rank_name"] == "Knight-Captain"


# ---- account update ----

def test_change_display_name(client):
    register(client)
    response = client.patch("/api/me", json={"display_name": "  Sir Jeff  "})
    assert response.status_code == 200
    assert response.json()["user"]["display_name"] == "Sir Jeff"
    assert client.get("/api/dashboard").json()["user"]["display_name"] == "Sir Jeff"
    assert client.patch("/api/me", json={"display_name": ""}).status_code == 422


def test_change_password_needs_the_current_one(client):
    register(client)
    wrong = client.post("/api/me/password", json={"current_password": "not-my-password", "new_password": "brand-new-pass-1"})
    assert wrong.status_code == 400
    short = client.post("/api/me/password", json={"current_password": ACCOUNT["password"], "new_password": "short"})
    assert short.status_code == 422


def test_new_password_works_and_the_old_one_stops(client):
    register(client)
    changed = client.post("/api/me/password", json={"current_password": ACCOUNT["password"], "new_password": "brand-new-pass-1"})
    assert changed.status_code == 204
    client.cookies.clear()
    email = ACCOUNT["email"]
    assert client.post("/api/auth/login", json={"email": email, "password": ACCOUNT["password"]}).status_code == 401
    assert client.post("/api/auth/login", json={"email": email, "password": "brand-new-pass-1"}).status_code == 200


def test_account_update_requires_signing_in(client):
    assert client.patch("/api/me", json={"display_name": "x"}).status_code == 401
    assert client.post("/api/me/password", json={"current_password": "a", "new_password": "brand-new-pass-1"}).status_code == 401


# ---- armory ----

def test_armory_requires_signing_in(client):
    assert client.get("/api/armory").status_code == 401
    assert client.post("/api/armory/buy", json={"item_id": "dragon-shield"}).status_code == 401
    assert client.put("/api/armory/loadout", json={"fighter": "knight", "item_id": None}).status_code == 401


def test_buying_gear_spends_coins(client):
    register(client)
    reach_squire(client)             # 55 coins
    response = client.post("/api/armory/buy", json={"item_id": "dragon-shield"})
    assert response.status_code == 200, response.text
    assert response.json()["user"]["coins"] == 25
    assert gear_item(response.json(), "dragon-shield")["owned"] is True


def test_cannot_buy_without_enough_coins(client):
    register(client)
    response = client.post("/api/armory/buy", json={"item_id": "dragon-shield"})
    assert response.status_code == 400
    assert client.get("/api/armory").json()["user"]["coins"] == 0
    assert gear_item(client.get("/api/armory").json(), "dragon-shield")["owned"] is False


def test_cannot_buy_twice_or_buy_rank_rewards_or_unknown_items(client):
    register(client)
    reach_squire(client)
    assert client.post("/api/armory/buy", json={"item_id": "dragon-shield"}).status_code == 200
    assert client.post("/api/armory/buy", json={"item_id": "dragon-shield"}).status_code == 409   # already owned
    assert client.post("/api/armory/buy", json={"item_id": "gold-armor"}).status_code == 409      # already unlocked by rank
    assert client.post("/api/armory/buy", json={"item_id": "flame-bow"}).status_code == 400       # rank reward, not for sale
    assert client.post("/api/armory/buy", json={"item_id": "excalibur"}).status_code == 404
    assert client.get("/api/armory").json()["user"]["coins"] == 25                                # charged once


def test_equip_swap_and_unequip(client):
    register(client)
    reach_squire(client)
    client.post("/api/armory/buy", json={"item_id": "dragon-shield"})

    equipped = client.put("/api/armory/loadout", json={"fighter": "knight", "item_id": "gold-armor"})
    assert equipped.status_code == 200, equipped.text
    assert equipped.json()["gear"]["loadout"] == {"knight": "gold-armor", "archer": None, "wizard": None}
    assert gear_item(equipped.json(), "gold-armor")["equipped"] is True

    swapped = client.put("/api/armory/loadout", json={"fighter": "knight", "item_id": "dragon-shield"}).json()
    assert swapped["gear"]["loadout"]["knight"] == "dragon-shield"
    assert gear_item(swapped, "gold-armor")["equipped"] is False

    removed = client.put("/api/armory/loadout", json={"fighter": "knight", "item_id": None}).json()
    assert removed["gear"]["loadout"]["knight"] is None
    assert client.get("/api/dashboard").json()["gear"]["loadout"]["knight"] is None


def test_cannot_equip_locked_gear_or_gear_for_another_fighter(client):
    register(client)
    reach_squire(client)
    assert client.put("/api/armory/loadout", json={"fighter": "wizard", "item_id": "storm-staff"}).status_code == 403
    assert client.put("/api/armory/loadout", json={"fighter": "archer", "item_id": "gold-armor"}).status_code == 400
    assert client.put("/api/armory/loadout", json={"fighter": "knight", "item_id": "excalibur"}).status_code == 404
    assert client.put("/api/armory/loadout", json={"fighter": "dragon", "item_id": None}).status_code == 422
    assert client.get("/api/armory").json()["gear"]["loadout"] == {"knight": None, "archer": None, "wizard": None}
