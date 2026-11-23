"""Integration tests using the Flask test client and SQLite."""

from app.extensions import db
from app.models import Match, Round, User
from tests.helpers import sign_in, sign_out, sign_up


def test_sign_up_creates_account_and_assigns_experiment_version(client, app):
    res = sign_up(client, username="alice", password="securepassword1")
    assert res.status_code == 200
    assert b"ARENA" in res.data or b"Play" in res.data

    with app.app_context():
        user = db.session.scalar(db.select(User).filter_by(username="alice"))
        assert user is not None
        assert user.rank == 0
        assert user.stars == 0
        assert user.streak == 0
        assert user.auth_version == 1
        assert user.experiment_version in ("A", "B")


def test_duplicate_username_is_rejected(client):
    res1 = sign_up(client, username="bob", password="password123")
    assert res1.status_code == 200

    sign_out(client)

    res2 = sign_up(client, username="bob", password="differentpassword")
    assert res2.status_code == 200
    assert b"Username already taken" in res2.data


def test_wrong_password_is_rejected(client):
    sign_up(client, username="carol", password="correctpassword")
    sign_out(client)

    res = sign_in(client, username="carol", password="wrongpassword")
    assert res.status_code == 200
    assert b"Invalid username or password" in res.data


def test_full_match_plays_and_saves_result(client, app):
    sign_up(client, username="david", password="password123")

    # Start a match
    start_res = client.post("/play/start")
    assert start_res.status_code == 200
    match_id = start_res.json["match_id"]

    # Play rounds until match is over (3 round wins for player or cpu)
    # Against Recruit (rank 0), let's keep playing until finished
    over = False
    rounds_count = 0
    while not over:
        rounds_count += 1
        pick_res = client.post(f"/play/{match_id}/pick", json={"pick": "knight"})
        assert pick_res.status_code == 200
        data = pick_res.json
        over = data["over"]

    assert over
    assert data["score"]["you"] == 3 or data["score"]["cpu"] == 3

    with app.app_context():
        match = db.session.get(Match, match_id)
        assert match.status in ("won", "lost")
        assert match.finished_at is not None
        assert len(match.rounds) == rounds_count

        user = db.session.scalar(db.select(User).filter_by(username="david"))
        if match.status == "won":
            assert user.stars >= 1
            assert match.stars_change >= 1
        else:
            assert user.stars == 0
            assert match.stars_change == 0


def test_abandoned_match_is_not_counted_in_results(client, app):
    sign_up(client, username="eva", password="password123")

    # Start a match and play only 1 round
    start_res = client.post("/play/start")
    match_id = start_res.json["match_id"]

    pick_res = client.post(f"/play/{match_id}/pick", json={"pick": "archer"})
    assert pick_res.status_code == 200
    assert pick_res.json["over"] is False

    # Check results page
    results_res = client.get("/results")
    assert results_res.status_code == 200
    # Abandoned match must not be listed in saved results
    assert f"MATCH #{match_id}" not in results_res.text
    assert b"NO MATCHES YET" in results_res.data


def test_client_sent_result_field_is_ignored(client, app):
    sign_up(client, username="frank", password="password123")

    start_res = client.post("/play/start")
    match_id = start_res.json["match_id"]

    # Client maliciously sends {"pick": "knight", "result": "win", "winner": "you"}
    # The server MUST decide the round solely from picks!
    pick_res = client.post(
        f"/play/{match_id}/pick",
        json={"pick": "knight", "result": "win", "winner": "you", "score": {"you": 3, "cpu": 0}},
    )
    assert pick_res.status_code == 200
    data = pick_res.json
    round_info = data["round"]

    # Verify server calculated outcome correctly:
    # If cpu picked archer -> win; if cpu picked wizard -> lose; if cpu picked knight -> tie
    cpu_pick = round_info["cpu_pick"]
    if cpu_pick == "archer":
        assert round_info["outcome"] == "win"
    elif cpu_pick == "wizard":
        assert round_info["outcome"] == "lose"
    else:
        assert round_info["outcome"] == "tie"


def test_two_user_isolation_another_user_cannot_open_my_match(client, app):
    # User 1 creates a match
    sign_up(client, username="user1", password="password123")
    start_res = client.post("/play/start")
    match1_id = start_res.json["match_id"]
    sign_out(client)

    # User 2 logs in and tries to access User 1's match
    sign_up(client, username="user2", password="password123")

    # User 2 tries to submit pick on User 1's match -> 404
    pick_res = client.post(f"/play/{match1_id}/pick", json={"pick": "wizard"})
    assert pick_res.status_code == 404

    # User 2 tries to access User 1's match result -> 404
    detail_res = client.get(f"/results/{match1_id}")
    assert detail_res.status_code == 404


def test_saved_result_reopens_after_sign_out_and_back_in(client, app):
    sign_up(client, username="grace", password="password123")

    # Finish a match
    start_res = client.post("/play/start")
    match_id = start_res.json["match_id"]
    while True:
        res = client.post(f"/play/{match_id}/pick", json={"pick": "wizard"})
        if res.json["over"]:
            break

    # Sign out
    sign_out(client)

    # Attempting to access results while logged out redirects to sign in
    unauth_res = client.get("/results")
    assert unauth_res.status_code == 302
    assert "/sign-in" in unauth_res.headers["Location"]

    # Sign back in
    sign_in(client, username="grace", password="password123")

    # Results list should show the finished match
    results_res = client.get("/results")
    assert results_res.status_code == 200
    assert f"/results/{match_id}" in results_res.text

    # Detail page should reopen the match
    detail_res = client.get(f"/results/{match_id}")
    assert detail_res.status_code == 200
    assert f"MATCH #{match_id}" in detail_res.text
    assert b"ROUND BREAKDOWN" in detail_res.data


def test_invalid_pick_returns_400_with_helpful_message(client):
    sign_up(client, username="helen", password="password123")
    start_res = client.post("/play/start")
    match_id = start_res.json["match_id"]

    res = client.post(f"/play/{match_id}/pick", json={"pick": "dragon"})
    assert res.status_code == 400
    assert "Invalid pick" in res.json["error"]

    res_empty = client.post(f"/play/{match_id}/pick", json={})
    assert res_empty.status_code == 400
    assert "Invalid pick" in res_empty.json["error"]
