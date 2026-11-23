"""Authentication blueprint for sign up, sign in, and sign out."""

import random

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_user, logout_user

from app.extensions import db
from app.forms import SignInForm, SignUpForm
from app.models import LoginSession, User

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/sign-in", methods=["GET", "POST"])
def sign_in():
    if current_user.is_authenticated:
        return redirect(url_for("play.play_screen"))

    form = SignInForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        user = db.session.scalar(db.select(User).filter_by(username=username))
        if user and user.check_password(form.password.data):
            login_user(user)
            session["auth_version"] = user.auth_version
            login_sess = LoginSession(user_id=user.id, auth_version=user.auth_version)
            db.session.add(login_sess)
            db.session.commit()
            next_url = request.args.get("next")
            return redirect(next_url or url_for("play.play_screen"))
        flash("Invalid username or password.", "error")

    return render_template("sign_in.html", form=form)


@auth_bp.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if current_user.is_authenticated:
        return redirect(url_for("play.play_screen"))

    form = SignUpForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        existing = db.session.scalar(db.select(User).filter_by(username=username))
        if existing:
            flash("Username already taken. Please choose another.", "error")
        else:
            exp_version = random.choice(["A", "B"])
            user = User(
                username=username,
                display_name=username,
                rank=0,
                stars=0,
                streak=0,
                auth_version=1,
                experiment_version=exp_version,
            )
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()

            login_user(user)
            session["auth_version"] = user.auth_version
            login_sess = LoginSession(user_id=user.id, auth_version=user.auth_version)
            db.session.add(login_sess)
            db.session.commit()

            return redirect(url_for("play.play_screen"))

    return render_template("sign_up.html", form=form)


@auth_bp.route("/sign-out", methods=["GET", "POST"])
def sign_out():
    logout_user()
    session.clear()
    return redirect(url_for("auth.sign_in"))
