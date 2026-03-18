"""Testing utilities and mock implementations for HydroMind contracts.

These mocks implement the core protocols and can be used by any downstream
package to write tests without depending on real engines or infrastructure.
"""

from hydromind_contracts.testing.mock_mcp import MockMCPClient
from hydromind_contracts.testing.mock_simulator import MockSimulator
from hydromind_contracts.testing.mock_controller import MockController
from hydromind_contracts.testing.mock_scada import MockSCADA
from hydromind_contracts.testing.mock_predictor import MockPredictor
from hydromind_contracts.testing.mock_scheduler import MockScheduler
from hydromind_contracts.testing.mock_detector import MockDetector
from hydromind_contracts.testing.mock_sensor import MockSensor
from hydromind_contracts.testing.mock_actuator import MockActuator
from hydromind_contracts.testing.mock_scada_protocol import MockScada
from hydromind_contracts.testing.mock_digital_twin import MockDigitalTwin

__all__ = [
    "MockMCPClient",
    "MockSimulator",
    "MockController",
    "MockSCADA",
    "MockPredictor",
    "MockScheduler",
    "MockDetector",
    "MockSensor",
    "MockActuator",
    "MockScada",
    "MockDigitalTwin",
]
