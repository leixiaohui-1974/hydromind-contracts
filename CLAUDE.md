# hydromind-contracts

Pure interface/protocol package for the HydroMind water network intelligence platform.

## Purpose

This package defines **all** inter-component contracts as Python `Protocol` classes.
It has **zero** runtime dependencies and serves as the single source of truth for
how HydroMind components communicate.

Any package in the HydroMind ecosystem should depend on `hydromind-contracts` for
type checking and interface compliance, but never the other way around.

## Protocols

| Module             | Protocols                                    |
|--------------------|----------------------------------------------|
| `simulation.py`    | `SimulatorProtocol`                          |
| `control.py`       | `ControllerProtocol`, `SafetyInterlockProtocol` |
| `prediction.py`    | `PredictorProtocol`                          |
| `scheduling.py`    | `SchedulerProtocol`                          |
| `identification.py`| `IdentifierProtocol`                         |
| `detection.py`     | `DetectorProtocol`, `LeakDetectorProtocol`   |
| `sensor.py`        | `SensorProtocol`, `SensorFusionProtocol`     |
| `actuator.py`      | `ActuatorProtocol`                           |
| `event.py`         | `EventProtocol`, `VisionEventProtocol`       |
| `agent.py`         | `AgentProtocol`, `AgentMessageProtocol`      |
| `skill.py`         | `SkillProtocol`                              |
| `mcp_tool.py`      | `MCPToolProtocol`                            |
| `digital_twin.py`  | `DigitalTwinProtocol`                        |

All protocols are `@runtime_checkable` and use only simple built-in types
(`dict`, `list`, `float`, `str`) -- no custom data classes.

## Registries

- `engine_registry.py` -- `discover_engines()`, `get_engine()` via `hydromind.engines` entry points.
- `role_registry.py` -- `discover_role_modules()`, `get_role_module()` via `hydromind.roles` entry points.

## Testing utilities (`hydromind_contracts.testing`)

- `MockMCPClient` -- register canned responses for MCP tool calls.
- `MockSimulator` -- implements `SimulatorProtocol`.
- `MockController` -- implements `ControllerProtocol`.
- `MockSCADA` -- tag read/write and alarm simulation for HydroGuard tests.

## Commands

- Install for development: `pip install -e ".[test]"`
- Run tests: `pytest`
