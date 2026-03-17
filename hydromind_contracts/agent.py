"""Agent protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class AgentProtocol(Protocol):
    """Contract for autonomous agents.

    Implementations encapsulate reasoning, planning, and action-selection
    logic for water network management tasks.
    """

    def process(self, message: dict) -> dict:
        """Process an incoming message and produce a response.

        Args:
            message: Structured message with at least a ``"content"`` key
                and optional ``"role"``, ``"context"`` keys.

        Returns:
            Dictionary containing:
                - ``response`` (str): Agent's textual response.
                - ``actions`` (list): Actions the agent wants to execute.
                - ``status`` (str): Processing status.
        """
        ...

    def get_capabilities(self) -> list:
        """Return the list of capabilities this agent supports.

        Returns:
            List of capability identifier strings.
        """
        ...


@runtime_checkable
class AgentMessageProtocol(Protocol):
    """Contract for inter-agent messaging.

    Implementations handle routing and delivery of messages between
    multiple agents in a multi-agent system.
    """

    def send(self, to: str, message: dict) -> dict:
        """Send a message to another agent.

        Args:
            to: Target agent identifier.
            message: Message payload.

        Returns:
            Dictionary with delivery status and message id.
        """
        ...

    def receive(self) -> dict:
        """Receive the next pending message.

        Returns:
            Dictionary with the message payload, sender id, and timestamp.
            Returns an empty dict if no messages are pending.
        """
        ...
