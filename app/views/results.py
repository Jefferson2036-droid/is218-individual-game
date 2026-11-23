"""Results blueprint: saved match history and match details."""

from flask import Blueprint, abort, render_template
from flask_login import current_user, login_required

from app.extensions import db
from app.game.progression import rank_name
from app.models import Match

results_bp = Blueprint("results", __name__, url_prefix="/results")


@results_bp.route("", methods=["GET"])
@login_required
def results_list():
    matches = (
        db.session.scalars(
            db.select(Match)
            .filter_by(user_id=current_user.id)
            .filter(Match.status.in_(["won", "lost"]))
            .order_by(Match.finished_at.desc(), Match.id.desc())
        )
        .all()
    )

    return render_template(
        "results.html",
        matches=matches,
        user=current_user,
        current_rank_name=rank_name(current_user.rank),
    )


@results_bp.route("/<int:match_id>", methods=["GET"])
@login_required
def result_detail(match_id: int):
    match = db.session.get(Match, match_id)
    if not match or match.user_id != current_user.id:
        abort(404)

    if match.status not in ("won", "lost"):
        abort(404)

    return render_template(
        "result_detail.html",
        match=match,
        user=current_user,
        opponent_rank=rank_name(match.rank_at_start),
    )
