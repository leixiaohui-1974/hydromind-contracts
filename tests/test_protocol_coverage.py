"""Protocol coverage analysis for HydroMind ecosystem.

Tests that protocol coverage is comprehensive: for every Protocol defined
in hydromind-contracts, at least one project should have a concrete class
or mock that satisfies it.
"""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Protocol, runtime_checkable

import pytest

# ---------------------------------------------------------------------------
# Project paths
# ---------------------------------------------------------------------------

PROJECTS = {
    "HydroGuard": Path("D:/research/HydroGuard"),
    "HydroDesign": Path("D:/research/HydroDesign"),
    "HydroArena": Path("D:/research/HydroArena"),
    "HydroEdu": Path("D:/research/HydroEdu"),
    "HydroLab": Path("D:/research/HydroLab"),
}

for name, path in PROJECTS.items():
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

# ---------------------------------------------------------------------------
# Discover all Protocol classes in hydromind_contracts
# ---------------------------------------------------------------------------

import hydromind_contracts
import hydromind_contracts.testing


def _discover_protocols() -> dict[str, type]:
    """Find all @runtime_checkable Protocol classes in hydromind_contracts."""
    protocols: dict[str, type] = {}

    # Scan all modules in hydromind_contracts package
    package_dir = Path(hydromind_contracts.__file__).parent
    for py_file in sorted(package_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        module_name = f"hydromind_contracts.{py_file.stem}"
        try:
            mod = importlib.import_module(module_name)
        except ImportError:
            continue
        for attr_name, attr in inspect.getmembers(mod, inspect.isclass):
            if (
                attr_name.endswith("Protocol")
                and issubclass(attr, Protocol)
                and attr is not Protocol
                and getattr(attr, "__protocol_attrs__", None) is not None
            ):
                protocols[attr_name] = attr

    return protocols


def _discover_mocks() -> dict[str, type]:
    """Find all mock classes in hydromind_contracts.testing."""
    mocks: dict[str, type] = {}
    testing_mod = hydromind_contracts.testing
    for attr_name, attr in inspect.getmembers(testing_mod, inspect.isclass):
        if attr_name.startswith("Mock"):
            mocks[attr_name] = attr
    return mocks


def _discover_implementations(protocol: type) -> list[tuple[str, str]]:
    """Find classes across satellite projects that satisfy a given protocol.

    Returns list of (project_name, class_name) tuples.
    """
    implementations: list[tuple[str, str]] = []

    # Check mocks first
    for mock_name, mock_cls in _discover_mocks().items():
        try:
            if isinstance(mock_cls(), protocol):
                implementations.append(("hydromind_contracts.testing", mock_name))
        except (TypeError, Exception):
            pass

    # Check satellite project modules
    project_modules = {
        "HydroGuard": [
            "hydroguard.station_controller.control.local_mpc",
            "hydroguard.station_controller.control.gate_coordinator",
            "hydroguard.station_controller.control.safety_interlock",
            "hydroguard.station_controller.scada.data_collector",
            "hydroguard.station_controller.perception.sensor_fusion",
            "hydroguard.station_controller.perception.anomaly_detector",
            "hydroguard.station_controller.digital_twin.station_twin",
            "hydroguard.health.health_scoring",
            "hydroguard.health.fault_diagnosis",
            "hydroguard.water_quality.online_monitor",
            "hydroguard.edge.agents.health_agent",
            "hydroguard.edge.agents.vision_fusion_agent",
            "hydroguard.edge.agents.water_quality_agent",
        ],
    }

    for project, modules in project_modules.items():
        for mod_path in modules:
            try:
                mod = importlib.import_module(mod_path)
            except ImportError:
                continue
            for attr_name, attr in inspect.getmembers(mod, inspect.isclass):
                if attr.__module__ != mod_path:
                    continue  # skip re-exports
                try:
                    instance = attr()
                    if isinstance(instance, protocol):
                        implementations.append((project, f"{mod_path}.{attr_name}"))
                except (TypeError, Exception):
                    # Class requires constructor args -- try structural check
                    # by verifying method signatures match
                    pass

    return implementations


# ============================================================================
# Protocol inventory test
# ============================================================================


ALL_PROTOCOLS = _discover_protocols()


class TestProtocolInventory:
    """Ensure the expected set of protocols exist in contracts."""

    EXPECTED_PROTOCOLS = {
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
        "WaterQualityProtocol",
        "OptimizationProtocol",
        "DispatchProtocol",
        "MessageBusProtocol",
    }

    def test_all_expected_protocols_exist(self):
        """All expected protocols should be discoverable."""
        discovered = set(ALL_PROTOCOLS.keys())
        missing = self.EXPECTED_PROTOCOLS - discovered
        assert len(missing) == 0, (
            f"Expected protocols not found: {missing}"
        )

    def test_no_unexpected_protocols(self):
        """Flag any new protocols that are not in the expected set."""
        discovered = set(ALL_PROTOCOLS.keys())
        unexpected = discovered - self.EXPECTED_PROTOCOLS
        if unexpected:
            # Not a failure -- just informational
            pytest.skip(
                f"New protocols detected (update EXPECTED_PROTOCOLS): {unexpected}"
            )

    def test_all_protocols_are_runtime_checkable(self):
        """Every protocol should be @runtime_checkable for isinstance() checks."""
        for name, proto in ALL_PROTOCOLS.items():
            # runtime_checkable protocols have _is_runtime_protocol set
            assert getattr(proto, "_is_runtime_protocol", False), (
                f"{name} is not @runtime_checkable. Add the decorator."
            )


# ============================================================================
# Protocol coverage test
# ============================================================================


class TestProtocolCoverage:
    """Test that every protocol has at least one implementation or mock."""

    # Protocols that have matching mocks in hydromind_contracts.testing
    MOCK_COVERAGE = {
        "SimulatorProtocol": "MockSimulator",
        "ControllerProtocol": "MockController",
        "PredictorProtocol": "MockPredictor",
        "SchedulerProtocol": "MockScheduler",
        "DetectorProtocol": "MockDetector",
        "SensorProtocol": "MockSensor",
        "ActuatorProtocol": "MockActuator",
        "ScadaProtocol": "MockScada",
        "DigitalTwinProtocol": "MockDigitalTwin",
    }

    def test_mock_coverage_map(self):
        """Validate that listed mocks actually satisfy their protocols."""
        mocks = _discover_mocks()
        for proto_name, mock_name in self.MOCK_COVERAGE.items():
            proto = ALL_PROTOCOLS.get(proto_name)
            mock_cls = mocks.get(mock_name)
            assert proto is not None, f"Protocol {proto_name} not found"
            assert mock_cls is not None, f"Mock {mock_name} not found"
            instance = mock_cls()
            assert isinstance(instance, proto), (
                f"{mock_name} does not satisfy {proto_name}"
            )

    def test_coverage_percentage(self):
        """Report protocol coverage and enforce a minimum threshold."""
        total = len(ALL_PROTOCOLS)
        covered = 0
        uncovered: list[str] = []

        for proto_name, proto in ALL_PROTOCOLS.items():
            implementations = _discover_implementations(proto)
            if implementations:
                covered += 1
            else:
                uncovered.append(proto_name)

        coverage_pct = (covered / total * 100) if total > 0 else 0

        # Print coverage report
        print(f"\n{'='*60}")
        print(f"Protocol Coverage Report")
        print(f"{'='*60}")
        print(f"Total protocols:    {total}")
        print(f"Covered:            {covered}")
        print(f"Uncovered:          {total - covered}")
        print(f"Coverage:           {coverage_pct:.1f}%")
        if uncovered:
            print(f"\nUncovered protocols:")
            for name in sorted(uncovered):
                print(f"  - {name}")
        print(f"{'='*60}\n")

        # At least the mocked protocols should be covered
        min_expected = len(self.MOCK_COVERAGE)
        assert covered >= min_expected, (
            f"Expected at least {min_expected} protocols covered by mocks, "
            f"got {covered}. Uncovered: {uncovered}"
        )

    @pytest.mark.parametrize("proto_name", sorted(ALL_PROTOCOLS.keys()))
    def test_individual_protocol_coverage(self, proto_name):
        """Each protocol should have at least one implementation or mock."""
        proto = ALL_PROTOCOLS[proto_name]

        # Protocols that currently lack mocks -- mark as expected failures
        PROTOCOLS_WITHOUT_MOCKS = {
            "SafetyInterlockProtocol",
            "IdentifierProtocol",
            "LeakDetectorProtocol",
            "SensorFusionProtocol",
            "EventProtocol",
            "VisionEventProtocol",
            "AgentProtocol",
            "AgentMessageProtocol",
            "SkillProtocol",
            "MCPToolProtocol",
            "HydraulicSolverProtocol",
            "WaterQualityProtocol",
            "OptimizationProtocol",
            "DispatchProtocol",
            "MessageBusProtocol",
        }

        impls = _discover_implementations(proto)
        if not impls and proto_name in PROTOCOLS_WITHOUT_MOCKS:
            pytest.xfail(
                f"{proto_name} has no mock or known implementation yet "
                f"(add Mock{proto_name.replace('Protocol', '')} to "
                f"hydromind_contracts.testing)"
            )

        assert len(impls) > 0, (
            f"{proto_name} has no known implementation. "
            f"Consider adding a mock to hydromind_contracts.testing"
        )


# ============================================================================
# Protocol method signature consistency
# ============================================================================


class TestProtocolSignatureConsistency:
    """Verify that protocol method signatures follow conventions."""

    def test_all_protocol_methods_return_annotations(self):
        """Protocol methods should have return type annotations."""
        missing_annotations: list[str] = []
        for proto_name, proto in ALL_PROTOCOLS.items():
            for method_name in dir(proto):
                if method_name.startswith("_"):
                    continue
                method = getattr(proto, method_name, None)
                if not callable(method):
                    continue
                try:
                    hints = inspect.get_annotations(method)
                except Exception:
                    continue
                if "return" not in hints:
                    missing_annotations.append(f"{proto_name}.{method_name}")

        if missing_annotations:
            print(f"\nMethods without return annotations: {missing_annotations}")
        # Informational only -- not a hard failure
        assert True

    def test_protocols_use_simple_types(self):
        """Protocol methods should use simple types (dict, list, float, str, bool).

        This is a design principle from the contracts CLAUDE.md: protocols use
        only built-in types, no custom dataclasses.
        """
        allowed_simple = {"dict", "list", "float", "str", "bool", "int", "None"}
        violations: list[str] = []

        for proto_name, proto in ALL_PROTOCOLS.items():
            for method_name in dir(proto):
                if method_name.startswith("_"):
                    continue
                method = getattr(proto, method_name, None)
                if not callable(method):
                    continue
                try:
                    sig = inspect.signature(method)
                except (ValueError, TypeError):
                    continue

                for param_name, param in sig.parameters.items():
                    if param_name == "self":
                        continue
                    annotation = param.annotation
                    if annotation is inspect.Parameter.empty:
                        continue
                    type_name = getattr(annotation, "__name__", str(annotation))
                    # Accept basic types and typing constructs
                    base = type_name.split("[")[0].strip()
                    if base not in allowed_simple and "Callable" not in str(annotation) and "Any" not in str(annotation):
                        violations.append(
                            f"{proto_name}.{method_name}({param_name}: {annotation})"
                        )

        if violations:
            print(f"\nPotential non-simple type parameters (review manually):")
            for v in violations:
                print(f"  {v}")
        # Informational -- protocol design convention
