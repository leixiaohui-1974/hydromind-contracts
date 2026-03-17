"""Verify that all protocols are runtime_checkable and that mocks satisfy them."""

import pytest

import hydromind_contracts as hc
from hydromind_contracts.testing import MockSimulator, MockController


# Collect every exported protocol class.
PROTOCOL_NAMES = [
    "SimulatorProtocol",
    "ControllerProtocol",
    "SafetyInterlockProtocol",
    "PredictorProtocol",
    "SchedulerProtocol",
    "IdentifierProtocol",
    "DetectorProtocol",
    "LeakDetectorProtocol",
    "SensorProtocol",
    "SensorFusionProtocol",
    "ActuatorProtocol",
    "EventProtocol",
    "VisionEventProtocol",
    "AgentProtocol",
    "AgentMessageProtocol",
    "SkillProtocol",
    "MCPToolProtocol",
    "DigitalTwinProtocol",
]


@pytest.mark.parametrize("name", PROTOCOL_NAMES)
def test_protocol_is_runtime_checkable(name: str) -> None:
    """Each protocol must be decorated with @runtime_checkable."""
    proto = getattr(hc, name)
    # runtime_checkable protocols have _is_runtime_protocol set to True.
    assert getattr(proto, "_is_runtime_protocol", False), (
        f"{name} is not @runtime_checkable"
    )


def test_mock_simulator_satisfies_protocol() -> None:
    sim = MockSimulator()
    assert isinstance(sim, hc.SimulatorProtocol)


def test_mock_controller_satisfies_protocol() -> None:
    ctrl = MockController()
    assert isinstance(ctrl, hc.ControllerProtocol)


def test_mock_simulator_simulate() -> None:
    sim = MockSimulator()
    result = sim.simulate({"roughness": 0.03}, duration=3600, dt=60)
    assert result["converged"] is True
    assert result["summary"]["steps"] == 60


def test_mock_controller_compute_action() -> None:
    ctrl = MockController()
    action = ctrl.compute_action(
        state={"level": 5.0},
        target={"level": 6.0},
        constraints={"max_gate": 1.0},
    )
    assert "actions" in action
    assert action["actions"]["level"] == 6.0
