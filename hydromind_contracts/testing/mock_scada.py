"""Mock SCADA interface for HydroGuard integration testing."""

from __future__ import annotations

from datetime import datetime, timezone


class MockSCADA:
    """A mock SCADA system for testing HydroGuard and other operational tools.

    Maintains an in-memory register of tag values that can be read and written,
    simulating a real SCADA/RTU layer.

    Example::

        scada = MockSCADA()
        scada.set_tag("gate_01.position", 0.5)
        reading = scada.read_tag("gate_01.position")
        assert reading["value"] == 0.5
    """

    def __init__(self) -> None:
        self._tags: dict[str, float] = {}
        self._alarms: list[dict] = []

    def set_tag(self, tag: str, value: float) -> None:
        """Set a SCADA tag value.

        Args:
            tag: Tag identifier.
            value: Numeric value.
        """
        self._tags[tag] = value

    def read_tag(self, tag: str) -> dict:
        """Read a SCADA tag.

        Args:
            tag: Tag identifier.

        Returns:
            Dictionary with ``value``, ``quality``, and ``timestamp``.
        """
        value = self._tags.get(tag)
        return {
            "tag": tag,
            "value": value,
            "quality": "good" if value is not None else "bad",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def read_all(self) -> dict:
        """Read all tag values.

        Returns:
            Dictionary mapping tag names to their current values.
        """
        return dict(self._tags)

    def trigger_alarm(self, tag: str, level: str, message: str) -> None:
        """Simulate a SCADA alarm.

        Args:
            tag: Tag that triggered the alarm.
            level: Severity level (``"info"``, ``"warning"``, ``"critical"``).
            message: Alarm description.
        """
        self._alarms.append(
            {
                "tag": tag,
                "level": level,
                "message": message,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def get_alarms(self) -> list[dict]:
        """Return all triggered alarms."""
        return list(self._alarms)

    def clear_alarms(self) -> None:
        """Clear the alarm buffer."""
        self._alarms.clear()
