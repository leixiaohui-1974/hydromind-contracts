"""Mock scheduler implementing SchedulerProtocol for testing."""

from __future__ import annotations


class MockScheduler:
    """A trivial scheduler that satisfies :class:`SchedulerProtocol`.

    Returns a feasible schedule with zero objective value for testing.
    """

    def __init__(self) -> None:
        self._last_network: dict = {}

    def optimize(self, network: dict, objectives: dict, constraints: dict) -> dict:
        """Compute a mock schedule echoing the network structure."""
        self._last_network = dict(network)
        assets = network.get("assets", ["asset_1"])
        schedule = {asset: [0.0] for asset in assets}
        return {
            "schedule": schedule,
            "objective_value": 0.0,
            "feasible": True,
            "metadata": {"solver": "mock", "iterations": 1},
        }
