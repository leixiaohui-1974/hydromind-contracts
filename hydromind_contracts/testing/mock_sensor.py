"""Mock sensor implementing SensorProtocol for testing."""

from __future__ import annotations

from datetime import datetime, timezone


class MockSensor:
    """A trivial sensor that satisfies :class:`SensorProtocol`.

    Maintains a configurable value that can be set for testing.
    """

    def __init__(
        self, value: float = 0.0, unit: str = "m", sensor_id: str = "mock_sensor"
    ) -> None:
        self._value = value
        self._unit = unit
        self._sensor_id = sensor_id
        self._online = True

    def set_value(self, value: float) -> None:
        """Set the sensor reading for testing."""
        self._value = value

    def set_online(self, online: bool) -> None:
        """Set the sensor online status."""
        self._online = online

    def read(self) -> dict:
        """Read the current mock sensor value."""
        return {
            "value": self._value,
            "unit": self._unit,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "quality": "good" if self._online else "bad",
        }

    def get_status(self) -> dict:
        """Return mock sensor status."""
        return {
            "online": self._online,
            "battery": 95.0,
            "last_seen": datetime.now(timezone.utc).isoformat(),
            "diagnostics": {"sensor_id": self._sensor_id},
        }
