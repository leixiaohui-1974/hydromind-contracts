"""Scheduling / optimization protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class SchedulerProtocol(Protocol):
    """Contract for network-level scheduling and optimization.

    Implementations solve optimal scheduling problems for pump stations,
    reservoir releases, inter-basin transfers, etc.
    """

    def optimize(self, network: dict, objectives: dict, constraints: dict) -> dict:
        """Compute an optimal schedule.

        Args:
            network: Network topology and current state description.
            objectives: Optimization objectives (minimize cost, maximize
                reliability, balance storage, etc.).
            constraints: Hard constraints (capacities, environmental flows,
                demand satisfaction, etc.).

        Returns:
            Dictionary containing:
                - ``schedule`` (dict): Time-indexed actions per asset.
                - ``objective_value`` (float): Achieved objective value.
                - ``feasible`` (bool): Whether a feasible solution was found.
                - ``metadata`` (dict): Solver statistics, gap, iterations.
        """
        ...
