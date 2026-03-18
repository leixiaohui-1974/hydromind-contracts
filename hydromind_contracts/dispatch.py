"""Dispatch protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class DispatchProtocol(Protocol):
    """Water dispatch/scheduling protocol."""

    def set_demands(self, demands: dict) -> None:
        """Set the water demand profile for scheduling.

        Args:
            demands: Dictionary mapping demand nodes to time-indexed demand
                values (flow rates, volumes, priorities, etc.).
        """
        ...

    def compute_schedule(self, horizon: int, dt: float) -> dict:
        """Compute a dispatch schedule over the planning horizon.

        Args:
            horizon: Number of time steps in the planning horizon.
            dt: Time step duration in seconds.

        Returns:
            Dictionary containing:
                - ``schedule`` (dict): Time-indexed dispatch actions per asset.
                - ``total_supply`` (float): Total water dispatched.
                - ``unmet_demand`` (float): Total unmet demand.
                - ``feasible`` (bool): Whether all demands can be satisfied.
        """
        ...

    def get_schedule(self) -> dict:
        """Retrieve the most recently computed schedule.

        Returns:
            Dictionary containing the last computed schedule, or an empty dict
            if no schedule has been computed yet.
        """
        ...
