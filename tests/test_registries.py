"""Tests for engine and role registries."""

from types import SimpleNamespace

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


def test_discover_role_modules_success_path(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeRole:
        pass

    fake_entry_point = SimpleNamespace(name="operator", load=lambda: FakeRole)
    monkeypatch.setattr(
        "hydromind_contracts.role_registry.entry_points",
        lambda: SimpleNamespace(select=lambda group: [fake_entry_point] if group == "hydromind.roles" else []),
    )
    result = discover_role_modules()
    assert "operator" in result
    assert result["operator"].load() is FakeRole


def test_get_role_module_success_path(monkeypatch: pytest.MonkeyPatch) -> None:
    class FakeRole:
        pass

    fake_entry_point = SimpleNamespace(name="designer", load=lambda: FakeRole)
    monkeypatch.setattr(
        "hydromind_contracts.role_registry.entry_points",
        lambda: SimpleNamespace(select=lambda group: [fake_entry_point] if group == "hydromind.roles" else []),
    )
    assert get_role_module("designer") is FakeRole
