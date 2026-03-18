"""Optimization protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class OptimizationProtocol(Protocol):
    """Multi-objective optimization protocol."""

    def set_objectives(self, objectives: list[dict]) -> None:
        """Define the optimization objectives.

        Args:
            objectives: List of objective specifications, each containing:
                - ``name`` (str): Objective name.
                - ``type`` (str): "minimize" or "maximize".
                - ``weight`` (float): Objective weight for aggregation.
        """
        ...

    def set_constraints(self, constraints: list[dict]) -> None:
        """Define the optimization constraints.

        Args:
            constraints: List of constraint specifications, each containing:
                - ``name`` (str): Constraint name.
                - ``type`` (str): "eq" or "ineq".
                - ``bounds`` (dict): Lower/upper bound values.
        """
        ...

    def optimize(self, config: dict) -> dict:
        """Run the optimization.

        Args:
            config: Solver configuration (algorithm, max iterations,
                tolerance, initial guess, etc.).

        Returns:
            Dictionary containing:
                - ``solution`` (dict): Optimal decision variables.
                - ``objective_values`` (dict): Achieved objective values.
                - ``feasible`` (bool): Whether a feasible solution was found.
                - ``metadata`` (dict): Solver statistics.
        """
        ...
