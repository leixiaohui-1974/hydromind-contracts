"""SCADA protocol contracts for HydroMind."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class ScadaProtocol(Protocol):
    """SCADA data collection protocol."""

    def connect(self, config: dict) -> bool:
        """Connect to a SCADA system.

        Args:
            config: Connection configuration (host, port, credentials, etc.).

        Returns:
            True if the connection was established successfully.
        """
        ...

    def read_points(self, point_ids: list[str]) -> dict:
        """Read multiple SCADA data points.

        Args:
            point_ids: List of point identifiers to read.

        Returns:
            Dictionary mapping point IDs to their current values and metadata.
        """
        ...

    def write_point(self, point_id: str, value: float) -> bool:
        """Write a value to a SCADA data point.

        Args:
            point_id: Point identifier.
            value: Value to write.

        Returns:
            True if the write was successful.
        """
        ...

    def disconnect(self) -> None:
        """Disconnect from the SCADA system."""
        ...
