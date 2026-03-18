"""Message bus protocol contracts for HydroMind."""

from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class MessageBusProtocol(Protocol):
    """Inter-agent message bus protocol."""

    def publish(self, topic: str, message: dict) -> None:
        """Publish a message to a topic.

        Args:
            topic: Topic name or channel.
            message: Message payload as a dictionary.
        """
        ...

    def subscribe(self, topic: str, handler: Any) -> None:
        """Subscribe to a topic with a handler callback.

        Args:
            topic: Topic name or channel to subscribe to.
            handler: Callable that receives message dicts when published.
        """
        ...

    def unsubscribe(self, topic: str) -> None:
        """Unsubscribe from a topic.

        Args:
            topic: Topic name or channel to unsubscribe from.
        """
        ...
