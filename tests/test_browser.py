"""Playwright browser tests for Arena Climb.

Journey: Sign up -> Play a match with keys 1/2/3 -> See result pop-up -> Open /results -> Sign out.
Screen width: 375 px (mobile viewport).
"""

import threading
import pytest
from werkzeug.serving import make_server

from app import create_app
from app.extensions import db
from tests.conftest import FixedRng


class ServerThread(threading.Thread):
    def __init__(self, app, port=0):
        super().__init__()
        self.server = make_server("127.0.0.1", port, app)
        self.port = self.server.port
        self.daemon = True

    def run(self):
        self.server.serve_forever()

    def shutdown(self):
        self.server.shutdown()


@pytest.fixture(scope="module")
def live_server():
    test_app = create_app(
        {
            "TESTING": True,
            "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
            "WTF_CSRF_ENABLED": False,
            "SECRET_KEY": "browser-test-secret-key",
            "RNG": FixedRng(index=0),  # Computer always picks Knight
        }
    )

    with test_app.app_context():
        db.create_all()

    server = ServerThread(test_app)
    server.start()

    yield f"http://127.0.0.1:{server.port}"

    server.shutdown()
    with test_app.app_context():
        db.drop_all()


def test_player_journey_mobile_viewport(live_server, page):
    # Set viewport to 375 px wide
    page.set_viewport_size({"width": 375, "height": 844})

    # 1. Sign up
    page.goto(f"{live_server}/sign-up")
    assert "ARENA" in page.content()

    page.fill("#username", "climb_hero")
    page.fill("#password", "password123")
    page.click("button[type='submit']")

    # 2. Battle Screen loads
    page.wait_for_url(f"{live_server}/play")
    assert page.is_visible("#arena-stage")
    assert page.is_visible("#round-narrative")

    # 3. Play a match using keys (computer plays Knight, so Wizard '3' wins)
    for round_num in range(3):
        # Wait until buttons are interactive
        page.wait_for_selector(".pick-btn:not(:disabled)", timeout=5000)
        with page.expect_response(lambda r: "/play/" in r.url and "/pick" in r.url and r.status == 200):
            page.keyboard.press("3")

        if round_num < 2:
            # Wait for round resolution and buttons to be re-enabled
            page.wait_for_selector(".pick-btn:not(:disabled)", timeout=5000)

    # 4. Result modal appears
    page.wait_for_selector("#result-modal", state="visible", timeout=6000)
    assert page.is_visible("#res-title")
    res_text = page.text_content("#res-title")
    assert "VICTORY" in res_text

    # 5. Open /results
    page.click("#modal-results-btn")
    page.wait_for_url(f"{live_server}/results")
    assert "SAVED MATCHES" in page.content()
    assert "3 – 0" in page.content() or "W" in page.content()

    # 6. Sign out
    page.click("#sign-out-btn")
    page.wait_for_url(f"{live_server}/sign-in")
    assert "SIGN IN" in page.content()
