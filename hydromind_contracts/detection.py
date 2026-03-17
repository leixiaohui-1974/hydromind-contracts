"""Detection protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class DetectorProtocol(Protocol):
    """Contract for anomaly / event detection.

    Implementations detect anomalies, faults, or notable events in
    monitoring data streams.
    """

    def detect(self, data: dict) -> dict:
        """Run detection on a data window.

        Args:
            data: Sensor readings or derived features for the detection
                window.

        Returns:
            Dictionary containing:
                - ``detected`` (bool): Whether an anomaly was found.
                - ``score`` (float): Detection confidence or severity score.
                - ``details`` (dict): Additional information (type, timestamp).
        """
        ...

    def localize(self, detection: dict) -> dict:
        """Localize a detected event in the network.

        Args:
            detection: Output from a prior ``detect()`` call.

        Returns:
            Dictionary containing:
                - ``location`` (str | dict): Identified location or region.
                - ``confidence`` (float): Localization confidence.
                - ``candidates`` (list): Ranked candidate locations.
        """
        ...


@runtime_checkable
class LeakDetectorProtocol(Protocol):
    """Specialized contract for leak detection and localization.

    Extends the general detection concept with leak-specific semantics
    such as estimated leak magnitude and pipe segment identification.
    """

    def detect(self, data: dict) -> dict:
        """Detect potential leaks from pressure/flow data.

        Args:
            data: Pressure and flow readings across the network.

        Returns:
            Dictionary containing:
                - ``leak_detected`` (bool): Whether a leak is suspected.
                - ``magnitude`` (float): Estimated leak flow rate.
                - ``confidence`` (float): Detection confidence.
        """
        ...

    def localize(self, detection: dict) -> dict:
        """Localize the leak to a pipe segment or zone.

        Args:
            detection: Output from ``detect()``.

        Returns:
            Dictionary containing:
                - ``pipe_id`` (str): Most likely pipe segment.
                - ``zone`` (str): Distribution zone.
                - ``candidates`` (list): Ranked candidate pipes with scores.
        """
        ...
