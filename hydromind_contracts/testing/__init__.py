"""Testing utilities and mock implementations for HydroMind contracts.

These mocks implement the core protocols and can be used by any downstream
package to write tests without depending on real engines or infrastructure.
"""

from hydromind_contracts.testing.mock_mcp import MockMCPClient
from hydromind_contracts.testing.mock_simulator import MockSimulator
from hydromind_contracts.testing.mock_controller import MockController
from hydromind_contracts.testing.mock_scada import MockSCADA

__all__ = [
    "MockMCPClient",
    "MockSimulator",
    "MockController",
    "MockSCADA",
]
