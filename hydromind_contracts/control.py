"""Control protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class ControllerProtocol(Protocol):
    """Contract for water network controllers.

    Implementations compute control actions (gate openings, pump speeds,
    valve positions) given the current system state and desired targets.
    """

    def compute_action(self, state: dict, target: dict, constraints: dict) -> dict:
        """Compute the next control action.

        Args:
            state: Current system state (levels, flows, pressures).
            target: Desired setpoints or objective values.
            constraints: Operational constraints (min/max values, ramp rates).

        Returns:
            Dictionary of control actions keyed by actuator identifier.
        """
        ...

    def set_target(self, targets: dict) -> None:
        """Update the control targets.

        Args:
            targets: New target setpoints keyed by variable name.
        """
        ...


@runtime_checkable
class SafetyInterlockProtocol(Protocol):
    """Contract for safety interlock logic.

    Implementations enforce hard safety limits that override normal control
    actions when dangerous conditions are detected.
    """

    def check(self, state: dict, proposed_action: dict) -> dict:
        """Check whether a proposed action is safe.

        Args:
            state: Current system state.
            proposed_action: The action the controller wants to execute.

        Returns:
            Dictionary with keys:
                - ``safe`` (bool): Whether the action is allowed.
                - ``modified_action`` (dict): Possibly clamped action.
                - ``violations`` (list): Descriptions of any violations.
        """
        ...

    def get_limits(self) -> dict:
        """Return the currently configured safety limits.

        Returns:
            Dictionary of limit specifications per variable/actuator.
        """
        ...
