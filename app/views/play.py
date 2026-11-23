"""Play blueprint: battle screen, match creation, and server-decided rounds."""

from flask import Blueprint, abort, current_app, jsonify, render_template, request
from flask_login import current_user, login_required

from app.extensions import db
from app.game.opponent import get_strategy
from app.game.progression import Progress, apply_match_result, rank_name, stars_needed
from app.game.rules import is_fighter, resolve
from app.models import Match, Round, now_utc

play_bp = Blueprint("play", __name__, url_prefix="/play")


@play_bp.route("", methods=["GET"])
@login_required
def play_screen():
    # Find active in-progress match or create a new one
    active_match = db.session.scalar(
        db.select(Match)
        .filter_by(user_id=current_user.id, status="in_progress")
        .order_by(Match.id.desc())
    )
    if not active_match:
        active_match = Match(
            user_id=current_user.id,
            status="in_progress",
            you=0,
            cpu=0,
            rank_at_start=current_user.rank,
            stars_at_start=current_user.stars,
            started_at=now_utc(),
        )
        db.session.add(active_match)
        db.session.commit()

    return render_template(
        "battle.html",
        match=active_match,
        user=current_user,
        current_rank_name=rank_name(current_user.rank),
        stars_needed=stars_needed(current_user.rank),
    )


@play_bp.route("/start", methods=["POST"])
@login_required
def start_match():
    # Create new in-progress match
    match = Match(
        user_id=current_user.id,
        status="in_progress",
        you=0,
        cpu=0,
        rank_at_start=current_user.rank,
        stars_at_start=current_user.stars,
        started_at=now_utc(),
    )
    db.session.add(match)
    db.session.commit()

    return jsonify(
        {
            "match_id": match.id,
            "status": match.status,
            "you": match.you,
            "cpu": match.cpu,
            "rank": current_user.rank,
            "stars": current_user.stars,
        }
    )


@play_bp.route("/<int:match_id>/pick", methods=["POST"])
@login_required
def submit_pick(match_id: int):
    match = db.session.get(Match, match_id)
    if not match or match.user_id != current_user.id:
        abort(404)

    if match.status != "in_progress":
        return jsonify({"error": "Match is already finished."}), 400

    # Accepts only pick in JSON or form data
    data = request.get_json(silent=True) or request.form
    pick = data.get("pick") if data else None

    if not pick or not is_fighter(pick):
        return jsonify({"error": "Invalid pick. Must be 'knight', 'archer', or 'wizard'."}), 400

    # Build rounds history for the AI
    match_rounds = [
        {"pick": r.player_pick, "cpu": r.cpu_pick, "result": r.outcome, "predicted": r.predicted}
        for r in match.rounds
    ]

    history_rounds = []
    if current_user.rank >= 3:
        # Champion uses earlier match rounds as well
        past_rounds = (
            db.session.query(Round)
            .join(Match)
            .filter(Match.user_id == current_user.id, Match.id != match.id)
            .order_by(Round.id.asc())
            .all()
        )
        history_rounds = [
            {"pick": r.player_pick, "cpu": r.cpu_pick, "result": r.outcome, "predicted": r.predicted}
            for r in past_rounds
        ]

    # Server selects computer move via rank strategy
    strategy = get_strategy(current_user.rank)
    rng = current_app.config.get("RNG")
    cpu_pick, predicted = strategy.choose(match_rounds, history_rounds, rng=rng)

    # Server decides the round
    outcome = resolve(pick, cpu_pick)

    round_n = len(match.rounds) + 1
    round_row = Round(
        match_id=match.id,
        n=round_n,
        player_pick=pick,
        cpu_pick=cpu_pick,
        outcome=outcome,
        predicted=predicted,
        created_at=now_utc(),
    )
    db.session.add(round_row)

    if outcome == "win":
        match.you += 1
    elif outcome == "lose":
        match.cpu += 1

    over = match.you >= 3 or match.cpu >= 3
    won = match.you >= 3
    progression_outcome = None

    if over:
        match.status = "won" if won else "lost"
        match.finished_at = now_utc()
        progression_outcome = apply_match_result(
            Progress(current_user.rank, current_user.stars, current_user.streak),
            won=won,
        )
        current_user.rank = progression_outcome.progress.rank
        current_user.stars = progression_outcome.progress.stars
        current_user.streak = progression_outcome.progress.streak

        match.rank_after = progression_outcome.progress.rank
        match.stars_after = progression_outcome.progress.stars
        match.stars_change = progression_outcome.stars_change

    db.session.commit()

    return jsonify(
        {
            "round": {
                "n": round_n,
                "player_pick": pick,
                "cpu_pick": cpu_pick,
                "outcome": outcome,
                "predicted": predicted,
            },
            "score": {"you": match.you, "cpu": match.cpu},
            "over": over,
            "won": won,
            "match_id": match.id,
            "stars_change": match.stars_change if over else 0,
            "ranked_up": progression_outcome.ranked_up if progression_outcome else False,
            "streak_bonus": progression_outcome.streak_bonus if progression_outcome else False,
            "player": {
                "rank": current_user.rank,
                "rank_name": rank_name(current_user.rank),
                "stars": current_user.stars,
                "stars_needed": stars_needed(current_user.rank),
                "streak": current_user.streak,
                "experiment_version": current_user.experiment_version,
            },
        }
    )
