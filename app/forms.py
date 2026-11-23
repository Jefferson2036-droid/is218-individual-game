"""Flask-WTF forms for authentication."""

from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField
from wtforms.validators import DataRequired, Length


class SignUpForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            DataRequired(message="Username is required."),
            Length(min=2, max=30, message="Username must be between 2 and 30 characters."),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(message="Password is required."),
            Length(min=6, message="Password must be at least 6 characters."),
        ],
    )


class SignInForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(message="Username is required.")])
    password = PasswordField("Password", validators=[DataRequired(message="Password is required.")])
