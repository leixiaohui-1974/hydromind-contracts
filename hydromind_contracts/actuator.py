"""Actuator protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ActuatorProtocol(Protocol):
    """Contract for actuator control (gates, pumps, valves).

    Implementations send commands to physical or simulated actuators
    and report their current position / state.
    """

    def execute(self, command: dict) -> dict:
        """Execute an actuator command.

        Args:
            command: Command specification, e.g.::

                {"action": "set_position", "value": 0.75, "unit": "fraction"}
                {"action": "start", "speed": 1200, "unit": "rpm"}

        Returns:
            Dictionary containing:
                - ``success`` (bool): Whether the command was accepted.
                - ``actual`` (float): Achieved value after execution.
                - ``timestamp`` (str): ISO-8601 execution timestamp.
                - ``error`` (str | None): Error message if unsuccessful.
        """
        ...

    def get_position(self) -> dict:
        """Return the current actuator position / operating point.

        Returns:
            Dictionary containing:
                - ``position`` (float): Current position or speed.
                - ``unit`` (str): Position unit.
                - ``mode`` (str): Operating mode (manual / auto / fault).
                - ``timestamp`` (str): ISO-8601 timestamp.
        """
        ...
