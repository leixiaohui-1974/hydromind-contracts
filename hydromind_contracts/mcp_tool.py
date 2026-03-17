"""MCP tool protocol contracts for HydroMind."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class MCPToolProtocol(Protocol):
    """Contract for Model Context Protocol (MCP) tool access.

    Implementations provide a uniform way to call tools exposed by MCP
    servers, abstracting transport and serialization details.
    """

    def call(self, tool_name: str, params: dict) -> dict:
        """Call an MCP tool.

        Args:
            tool_name: Fully qualified tool name.
            params: Tool input parameters.

        Returns:
            Dictionary containing the tool's response payload.
        """
        ...

    def list_tools(self) -> list:
        """List all available tools on the connected MCP server(s).

        Returns:
            List of tool descriptors (dicts with ``name``, ``description``,
            ``inputSchema`` keys).
        """
        ...
