"""Shapes of the data the API accepts."""

from typing import Literal, Optional

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


class ProfileIn(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    display_name: str = Field(min_length=1, max_length=40)


class PasswordIn(BaseModel):
    current_password: str = Field(max_length=128)
    new_password: str = Field(min_length=8, max_length=128)


class BuyIn(BaseModel):
    item_id: str = Field(max_length=40)


class LoadoutIn(BaseModel):
    fighter: Literal["knight", "archer", "wizard"]
    item_id: Optional[str] = Field(default=None, max_length=40)   # None takes the gear off
