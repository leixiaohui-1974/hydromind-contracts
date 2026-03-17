"""Simulation protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class SimulatorProtocol(Protocol):
    """Contract for hydraulic/hydrological simulators.

    Implementations wrap simulation engines (e.g., SWMM, HEC-RAS, EPANET)
    behind a uniform interface so that higher-level orchestration code never
    depends on a specific engine.
    """

    def simulate(self, params: dict, duration: float, dt: float) -> dict:
        """Run a simulation.

        Args:
            params: Model parameters and initial conditions.
            duration: Simulation duration in seconds.
            dt: Time step in seconds.

        Returns:
            Dictionary containing simulation results (time series, summary
            statistics, convergence info, etc.).
        """
        ...

    def get_state(self) -> dict:
        """Return the current internal state of the simulator.

        Returns:
            Dictionary with state variables (levels, flows, pressures, etc.).
        """
        ...

    def set_boundary(self, conditions: dict) -> None:
        """Set boundary conditions for the next simulation run.

        Args:
            conditions: Boundary condition specification (inflows, water
                levels, meteorological forcing, etc.).
        """
        ...
