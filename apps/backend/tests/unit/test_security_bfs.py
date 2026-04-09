"""Unit: хешування та JWT (логіка як на бекенді для login / захищених сторінок)."""

import pytest

from app.core.security import (
    create_access_token,
    decode_access_token,
    get_sub_from_token,
    hash_password,
    verify_password,
)


def test_bfs_security_password_hash_verify_roundtrip() -> None:
    h = hash_password("MyPass1a")
    assert verify_password("MyPass1a", h) is True


def test_bfs_security_verify_rejects_wrong_password() -> None:
    h = hash_password("Correct1a")
    assert verify_password("Wrong1a", h) is False


def test_bfs_security_access_token_decode_roundtrip() -> None:
    token = create_access_token(subject="42", email="u@example.com")
    payload = decode_access_token(token)
    assert payload["sub"] == "42"
    assert payload["email"] == "u@example.com"
    assert "exp" in payload


def test_bfs_security_get_sub_from_invalid_token_raises() -> None:
    with pytest.raises(ValueError, match="invalid token"):
        get_sub_from_token("not-a-jwt")


def test_bfs_security_get_sub_from_valid_token_returns_user_id() -> None:
    token = create_access_token(subject="7", email="seven@example.com")
    assert get_sub_from_token(token) == 7
