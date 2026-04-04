"""Unit: валідація реєстрації (як на сторінці register / login flow)."""

import pytest
from pydantic import ValidationError

from app.schemas.user import UserRegister


def test_bfs_user_register_password_requires_letter_and_digit() -> None:
    with pytest.raises(ValidationError):
        UserRegister(name="A", email="a@b.co", password="12345678")
    with pytest.raises(ValidationError):
        UserRegister(name="A", email="a@b.co", password="abcdefgh")


def test_bfs_user_register_name_whitespace_only_rejected_like_empty_form() -> None:
    with pytest.raises(ValidationError):
        UserRegister(name="   ", email="a@b.co", password="secret1a")
