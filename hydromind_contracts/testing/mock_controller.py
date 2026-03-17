"""Mock controller implementing ControllerProtocol for testing."""

from __future__ import annotations


class MockController:
    """A trivial controller that satisfies :class:`ControllerProtocol`.

    Returns zero-action by default. Useful for testing control pipelines
    without real control algorithms.
    """

    def __init__(self) -> None:
        self._targets: dict = {}

    def compute_action(
        self, state: dict, target: dict, constraints: dict
    ) -> dict:
        """Compute a mock action (echoes target as action)."""
        return {
            "actions": {k: v for k, v in target.items()},
            "state_received": bool(state),
            "constrained": bool(constraints),
        }

    def set_target(self, targets: dict) -> None:
        """Store targets."""
        self._targets = dict(targets)
