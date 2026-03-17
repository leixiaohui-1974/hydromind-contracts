"""Skill protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class SkillProtocol(Protocol):
    """Contract for agent skills / capabilities.

    A skill is a discrete, reusable unit of functionality that an agent
    can invoke. Each skill exposes the tools it needs and an execute method.
    """

    def execute(self, params: dict) -> dict:
        """Execute the skill with the given parameters.

        Args:
            params: Skill-specific input parameters.

        Returns:
            Dictionary containing:
                - ``result`` (dict): Skill output.
                - ``success`` (bool): Whether execution succeeded.
                - ``logs`` (list): Execution log entries.
        """
        ...

    def get_tools(self) -> list:
        """Return the list of tools this skill requires or provides.

        Returns:
            List of tool descriptors (dicts with ``name``, ``description``,
            ``parameters`` keys).
        """
        ...
