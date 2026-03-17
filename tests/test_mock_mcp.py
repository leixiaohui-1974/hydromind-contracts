"""Tests for MockMCPClient."""

import pytest

from hydromind_contracts.testing import MockMCPClient


def test_default_response() -> None:
    client = MockMCPClient()
    result = client.call_sync("any-server", "any-tool")
    assert result["status"] == "mock"
    assert result["server"] == "any-server"
    assert result["tool"] == "any-tool"


def test_registered_dict_response() -> None:
    client = MockMCPClient()
    client.register_response("sim", "run", {"status": "ok", "steps": 100})
    result = client.call_sync("sim", "run")
    assert result["status"] == "ok"
    assert result["steps"] == 100


def test_registered_callable_response() -> None:
    client = MockMCPClient()
    client.register_response(
        "sim", "run", lambda params: {"echo": params}
    )
    result = client.call_sync("sim", "run", {"dt": 60})
    assert result["echo"]["dt"] == 60


@pytest.mark.asyncio
async def test_async_call() -> None:
    client = MockMCPClient()
    client.register_response("ctrl", "set", {"done": True})
    result = await client.call("ctrl", "set", {"target": 5.0})
    assert result["done"] is True
