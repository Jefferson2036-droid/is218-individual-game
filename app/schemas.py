"""Shapes of the data the API accepts."""

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class RegisterIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str = Field(max_length=254, pattern=EMAIL_PATTERN)
    password: str = Field(min_length=8, max_length=128)
    display_name: str = Field(min_length=1, max_length=40)


class LoginIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    email: str = Field(max_length=254)
    password: str = Field(max_length=128)


class PickIn(BaseModel):
    pick: Literal["knight", "archer", "wizard"]
