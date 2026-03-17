"""Tests for engine and role registries."""

import pytest

from hydromind_contracts.engine_registry import discover_engines, get_engine
from hydromind_contracts.role_registry import discover_role_modules, get_role_module


def test_discover_engines_returns_dict() -> None:
    """discover_engines should return a dict (possibly empty)."""
    result = discover_engines()
    assert isinstance(result, dict)


def test_discover_role_modules_returns_dict() -> None:
    """discover_role_modules should return a dict (possibly empty)."""
    result = discover_role_modules()
    assert isinstance(result, dict)


def test_get_engine_missing_raises() -> None:
    """Requesting a non-existent engine should raise KeyError."""
    with pytest.raises(KeyError, match="not found"):
        get_engine("nonexistent_engine_xyz")


def test_get_role_module_missing_raises() -> None:
    """Requesting a non-existent role should raise KeyError."""
    with pytest.raises(KeyError, match="not found"):
        get_role_module("nonexistent_role_xyz")


def test_get_engine_env_override(monkeypatch: pytest.MonkeyPatch) -> None:
    """HYDROMIND_ENGINE env var should override the name parameter."""
    monkeypatch.setenv("HYDROMIND_ENGINE", "phantom_engine")
    with pytest.raises(KeyError, match="phantom_engine"):
        get_engine("other")
