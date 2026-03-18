"""Mock digital twin implementing DigitalTwinProtocol for testing."""

from __future__ import annotations

from datetime import datetime, timezone


class MockDigitalTwin:
    """A trivial digital twin that satisfies :class:`DigitalTwinProtocol`.

    Tracks a synced state and returns mock predictions for testing.
    """

    def __init__(self) -> None:
        self._state: dict = {}
        self._synced = False
        self._drift = 0.0

    def sync(self, real_state: dict) -> dict:
        """Synchronize with the provided real-world state."""
        self._drift = 0.01 if self._state else 0.0
        self._state = dict(real_state)
        self._synced = True
        return {
            "synced": True,
            "drift": self._drift,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def predict(self, duration: float) -> dict:
        """Generate a mock forward prediction from the current state."""
        n_steps = max(1, int(duration / 60.0))
        states = [dict(self._state) for _ in range(n_steps)]
        return {
            "states": states,
            "horizon": duration,
            "confidence": 0.92 if self._synced else 0.5,
        }

    def get_discrepancy(self) -> dict:
        """Return mock discrepancy information."""
        return {
            "variables": {k: 0.01 for k in self._state},
            "overall": self._drift,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
