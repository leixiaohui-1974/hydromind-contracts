"""HydroMind Contracts -- pure interface / protocol package.

This package defines all Protocol classes (interfaces) for the HydroMind
water network intelligence platform.  It has **zero** runtime dependencies
and is intended to be the single source of truth for inter-component contracts.
"""

__version__ = "0.1.0"

# --- Protocols -----------------------------------------------------------
from hydromind_contracts.simulation import SimulatorProtocol
from hydromind_contracts.control import ControllerProtocol, SafetyInterlockProtocol
from hydromind_contracts.prediction import PredictorProtocol
from hydromind_contracts.scheduling import SchedulerProtocol
from hydromind_contracts.identification import IdentifierProtocol
from hydromind_contracts.detection import DetectorProtocol, LeakDetectorProtocol
from hydromind_contracts.sensor import SensorProtocol, SensorFusionProtocol
from hydromind_contracts.actuator import ActuatorProtocol
from hydromind_contracts.event import EventProtocol, VisionEventProtocol
from hydromind_contracts.agent import AgentProtocol, AgentMessageProtocol
from hydromind_contracts.skill import SkillProtocol
from hydromind_contracts.mcp_tool import MCPToolProtocol
from hydromind_contracts.digital_twin import DigitalTwinProtocol
from hydromind_contracts.scada import ScadaProtocol
from hydromind_contracts.hydraulic_solver import (
    ChannelConfigProtocol,
    HydraulicSolverProtocol,
)
from hydromind_contracts.water_quality import WaterQualityProtocol
from hydromind_contracts.optimization import OptimizationProtocol
from hydromind_contracts.dispatch import DispatchProtocol
from hydromind_contracts.message_bus import MessageBusProtocol

# --- Registries ----------------------------------------------------------
from hydromind_contracts.engine_registry import discover_engines, get_engine
from hydromind_contracts.role_registry import discover_role_modules, get_role_module

__all__ = [
    # Protocols
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
    "ScadaProtocol",
    "HydraulicSolverProtocol",
    "ChannelConfigProtocol",
    "WaterQualityProtocol",
    "OptimizationProtocol",
    "DispatchProtocol",
    "MessageBusProtocol",
    # Registries
    "discover_engines",
    "get_engine",
    "discover_role_modules",
    "get_role_module",
]
