"""Mock MCP client for testing MCP tool interactions."""

from __future__ import annotations

import asyncio
from typing import Any, Callable


class MockMCPClient:
    """A test double for MCP server interactions.

    Register canned responses (or callables) for ``(server, tool)`` pairs,
    then call them synchronously or asynchronously during tests.

    Example::

        client = MockMCPClient()
        client.register_response("hydro-sim", "run", {"status": "ok"})
        result = client.call_sync("hydro-sim", "run", {"dt": 60})
        assert result["status"] == "ok"
    """

    def __init__(self) -> None:
        self._responses: dict[tuple[str, str], Any] = {}

    def register_response(
        self, server: str, tool: str, response: dict | Callable
    ) -> None:
        """Register a canned response for a server/tool pair.

        Args:
            server: MCP server name.
            tool: Tool name on that server.
            response: Either a dict to return directly, or a callable that
                receives ``params`` and returns a dict.
        """
        self._responses[(server, tool)] = response

    async def call(
        self, server: str, tool: str, params: dict | None = None
    ) -> dict:
        """Asynchronously call a registered tool.

        Args:
            server: MCP server name.
            tool: Tool name.
            params: Tool parameters.

        Returns:
            The registered response, or a default mock response.
        """
        key = (server, tool)
        if key in self._responses:
            resp = self._responses[key]
            return resp(params) if callable(resp) else resp
        return {"status": "mock", "server": server, "tool": tool}

    def call_sync(
        self, server: str, tool: str, params: dict | None = None
    ) -> dict:
        """Synchronous wrapper around :meth:`call` for simple test code.

        Args:
            server: MCP server name.
            tool: Tool name.
            params: Tool parameters.

        Returns:
            The registered response, or a default mock response.
        """
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            # Already inside an event loop -- create a new one in a thread.
            import concurrent.futures

            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(
                    asyncio.run, self.call(server, tool, params)
                )
                return future.result()
        else:
            return asyncio.run(self.call(server, tool, params))
