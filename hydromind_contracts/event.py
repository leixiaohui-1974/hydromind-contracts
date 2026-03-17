"""Event protocol contracts for HydroMind."""

from typing import Any, Callable, Protocol, runtime_checkable


@runtime_checkable
class EventProtocol(Protocol):
    """Contract for event emission and subscription.

    Implementations provide a lightweight pub/sub mechanism for decoupled
    communication between HydroMind components.
    """

    def emit(self, event_type: str, data: dict) -> None:
        """Emit an event.

        Args:
            event_type: Event type identifier (e.g. ``"alarm.high_level"``).
            data: Event payload.
        """
        ...

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to events of a given type.

        Args:
            event_type: Event type to listen for.
            callback: Callable invoked with ``(event_type, data)`` when
                the event fires.
        """
        ...


@runtime_checkable
class VisionEventProtocol(Protocol):
    """Contract for vision-based event analysis.

    Implementations analyze camera frames or image data to detect and
    classify events (e.g., floating debris, ice formation, intrusion).
    """

    def analyze_frame(self, frame: Any) -> dict:
        """Analyze a single video/image frame.

        Args:
            frame: Image data (numpy array, bytes, or file path).

        Returns:
            Dictionary containing:
                - ``events`` (list): Detected events with type and bbox.
                - ``timestamp`` (str): Frame timestamp.
                - ``confidence`` (float): Overall detection confidence.
        """
        ...
