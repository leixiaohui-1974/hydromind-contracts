"""Sensor protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class SensorProtocol(Protocol):
    """Contract for individual sensor access.

    Implementations wrap physical or virtual sensors (water level gauges,
    flow meters, pressure transducers, rain gauges, etc.).
    """

    def read(self) -> dict:
        """Read the current sensor value.

        Returns:
            Dictionary containing:
                - ``value`` (float): The measured value.
                - ``unit`` (str): Measurement unit.
                - ``timestamp`` (str): ISO-8601 timestamp of the reading.
                - ``quality`` (str): Data quality flag.
        """
        ...

    def get_status(self) -> dict:
        """Return sensor health / status information.

        Returns:
            Dictionary containing:
                - ``online`` (bool): Whether the sensor is reachable.
                - ``battery`` (float | None): Battery level percentage.
                - ``last_seen`` (str): ISO-8601 timestamp of last contact.
                - ``diagnostics`` (dict): Vendor-specific diagnostics.
        """
        ...


@runtime_checkable
class SensorFusionProtocol(Protocol):
    """Contract for multi-sensor data fusion.

    Implementations combine readings from multiple sensors to produce
    a more accurate or complete estimate of the measured quantity.
    """

    def fuse(self, readings: list) -> dict:
        """Fuse multiple sensor readings.

        Args:
            readings: List of individual sensor reading dicts (as returned
                by ``SensorProtocol.read()``).

        Returns:
            Dictionary containing:
                - ``value`` (float): Fused estimate.
                - ``unit`` (str): Measurement unit.
                - ``sources`` (int): Number of contributing sensors.
                - ``method`` (str): Fusion algorithm used.
        """
        ...

    def get_confidence(self) -> float:
        """Return the confidence level of the last fusion result.

        Returns:
            A float in [0, 1] representing fusion confidence.
        """
        ...
