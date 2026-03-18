"""Mock detector implementing DetectorProtocol for testing."""

from __future__ import annotations


class MockDetector:
    """A trivial detector that satisfies :class:`DetectorProtocol`.

    Never detects anomalies by default. Call ``set_detected(True)`` to
    simulate an anomaly for testing.
    """

    def __init__(self) -> None:
        self._detected: bool = False
        self._score: float = 0.0

    def set_detected(self, detected: bool, score: float = 0.95) -> None:
        """Configure whether the next detect() call finds an anomaly."""
        self._detected = detected
        self._score = score if detected else 0.0

    def detect(self, data: dict) -> dict:
        """Run mock detection."""
        return {
            "detected": self._detected,
            "score": self._score,
            "details": {"type": "mock", "data_keys": list(data.keys())},
        }

    def localize(self, detection: dict) -> dict:
        """Return a mock localization result."""
        return {
            "location": "mock_zone_A",
            "confidence": 0.85 if detection.get("detected") else 0.0,
            "candidates": [
                {"location": "mock_zone_A", "score": 0.85},
                {"location": "mock_zone_B", "score": 0.10},
            ],
        }
