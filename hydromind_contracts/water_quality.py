"""Water quality protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class WaterQualityProtocol(Protocol):
    """Water quality simulation protocol."""

    def set_sources(self, sources: dict) -> None:
        """Configure pollutant sources in the network.

        Args:
            sources: Dictionary mapping node IDs to source specifications
                (concentration, mass injection rate, pattern, etc.).
        """
        ...

    def simulate(self, duration: float, dt: float) -> dict:
        """Run a water quality simulation.

        Args:
            duration: Simulation duration in seconds.
            dt: Time step in seconds.

        Returns:
            Dictionary containing:
                - ``time_series`` (list): Time stamps.
                - ``concentrations`` (dict): Node-level concentration histories.
                - ``converged`` (bool): Whether the simulation completed normally.
        """
        ...

    def get_concentrations(self, nodes: list[str]) -> dict:
        """Get current concentrations at specified nodes.

        Args:
            nodes: List of node identifiers.

        Returns:
            Dictionary mapping node IDs to concentration values and metadata.
        """
        ...
