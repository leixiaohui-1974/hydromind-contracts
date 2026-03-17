"""Mock simulator implementing SimulatorProtocol for testing."""

from __future__ import annotations


class MockSimulator:
    """A trivial simulator that satisfies :class:`SimulatorProtocol`.

    Useful for testing orchestration logic without a real simulation engine.
    """

    def __init__(self) -> None:
        self._state: dict = {}
        self._boundary: dict = {}

    def simulate(self, params: dict, duration: float, dt: float) -> dict:
        """Run a mock simulation that simply stores params and returns them."""
        steps = int(duration / dt) if dt > 0 else 0
        self._state = {
            "params": params,
            "duration": duration,
            "dt": dt,
            "steps": steps,
        }
        return {
            "time_series": [0.0] * steps,
            "summary": {"steps": steps, "duration": duration},
            "converged": True,
        }

    def get_state(self) -> dict:
        """Return the current mock state."""
        return dict(self._state)

    def set_boundary(self, conditions: dict) -> None:
        """Store boundary conditions."""
        self._boundary = dict(conditions)
