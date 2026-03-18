"""Mock SCADA implementing ScadaProtocol for testing."""

from __future__ import annotations

from datetime import datetime, timezone


class MockScada:
    """A mock SCADA client that satisfies :class:`ScadaProtocol`.

    Maintains an in-memory register of data points for testing SCADA
    interactions without a real SCADA/RTU system.
    """

    def __init__(self) -> None:
        self._connected = False
        self._config: dict = {}
        self._points: dict[str, float] = {}

    def connect(self, config: dict) -> bool:
        """Simulate connecting to a SCADA system."""
        self._config = dict(config)
        self._connected = True
        return True

    def read_points(self, point_ids: list[str]) -> dict:
        """Read multiple data points from the mock register."""
        results: dict = {}
        for pid in point_ids:
            value = self._points.get(pid)
            results[pid] = {
                "value": value,
                "quality": "good" if value is not None else "bad",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        return results

    def write_point(self, point_id: str, value: float) -> bool:
        """Write a value to the mock register."""
        if not self._connected:
            return False
        self._points[point_id] = value
        return True

    def disconnect(self) -> None:
        """Simulate disconnecting from the SCADA system."""
        self._connected = False

    # ---- Test helpers ----

    def set_point(self, point_id: str, value: float) -> None:
        """Pre-populate a data point for testing."""
        self._points[point_id] = value

    @property
    def is_connected(self) -> bool:
        """Whether the mock client is in connected state."""
        return self._connected
