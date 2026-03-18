"""Mock actuator implementing ActuatorProtocol for testing."""

from __future__ import annotations

from datetime import datetime, timezone


class MockActuator:
    """A trivial actuator that satisfies :class:`ActuatorProtocol`.

    Accepts any command and tracks its position for testing.
    """

    def __init__(self, position: float = 0.0, unit: str = "fraction") -> None:
        self._position = position
        self._unit = unit
        self._mode = "auto"

    def execute(self, command: dict) -> dict:
        """Execute a mock actuator command."""
        action = command.get("action", "set_position")
        value = command.get("value", self._position)
        self._position = float(value)
        return {
            "success": True,
            "actual": self._position,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "error": None,
        }

    def get_position(self) -> dict:
        """Return the current mock actuator position."""
        return {
            "position": self._position,
            "unit": self._unit,
            "mode": self._mode,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
