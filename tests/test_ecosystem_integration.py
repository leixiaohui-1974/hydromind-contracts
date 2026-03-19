"""Cross-project integration tests for HydroMind ecosystem.

Tests that satellite projects properly implement hydromind-contracts protocols.
Validates protocol compliance, role module interfaces, MCP tool schemas,
mock compatibility, and entry point configuration across all projects.
"""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Any, get_type_hints

import pytest

# ---------------------------------------------------------------------------
# Project path setup
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
# Import contracts
# ---------------------------------------------------------------------------

from hydromind_contracts import (
    ActuatorProtocol,
    AgentMessageProtocol,
    AgentProtocol,
    ControllerProtocol,
    DetectorProtocol,
    DigitalTwinProtocol,
    DispatchProtocol,
    EventProtocol,
    HydraulicSolverProtocol,
    IdentifierProtocol,
    LeakDetectorProtocol,
    MCPToolProtocol,
    MessageBusProtocol,
    OptimizationProtocol,
    PredictorProtocol,
    SafetyInterlockProtocol,
    ScadaProtocol,
    SchedulerProtocol,
    SensorFusionProtocol,
    SensorProtocol,
    SimulatorProtocol,
    SkillProtocol,
    VisionEventProtocol,
    WaterQualityProtocol,
)

from hydromind_contracts.testing import (
    MockActuator,
    MockController,
    MockDetector,
    MockDigitalTwin,
    MockMCPClient,
    MockPredictor,
    MockScada,
    MockScheduler,
    MockSensor,
    MockSimulator,
)


# ============================================================================
# 1. Protocol Compliance Tests
# ============================================================================


class TestSimulatorProtocolCompliance:
    """Verify MockSimulator satisfies SimulatorProtocol."""

    def test_isinstance_check(self):
        sim = MockSimulator()
        assert isinstance(sim, SimulatorProtocol), (
            "MockSimulator must satisfy SimulatorProtocol"
        )

    def test_simulate_returns_dict(self):
        sim = MockSimulator()
        result = sim.simulate(params={"level": 5.0}, duration=100.0, dt=10.0)
        assert isinstance(result, dict)
        assert "time_series" in result
        assert "converged" in result

    def test_get_state_returns_dict(self):
        sim = MockSimulator()
        sim.simulate(params={"q": 1.0}, duration=60.0, dt=1.0)
        state = sim.get_state()
        assert isinstance(state, dict)
        assert "params" in state

    def test_set_boundary_accepts_dict(self):
        sim = MockSimulator()
        sim.set_boundary({"inflow": 10.0, "water_level": 3.5})
        # Should not raise


class TestControllerProtocolCompliance:
    """Verify MockController satisfies ControllerProtocol."""

    def test_isinstance_check(self):
        ctrl = MockController()
        assert isinstance(ctrl, ControllerProtocol), (
            "MockController must satisfy ControllerProtocol"
        )

    def test_compute_action_returns_dict(self):
        ctrl = MockController()
        action = ctrl.compute_action(
            state={"level": 2.0},
            target={"level": 3.0},
            constraints={"max_gate": 1.0},
        )
        assert isinstance(action, dict)
        assert "actions" in action

    def test_set_target_accepts_dict(self):
        ctrl = MockController()
        ctrl.set_target({"level": 3.0, "flow": 5.0})


class TestSensorProtocolCompliance:
    """Verify MockSensor satisfies SensorProtocol."""

    def test_isinstance_check(self):
        sensor = MockSensor()
        assert isinstance(sensor, SensorProtocol), (
            "MockSensor must satisfy SensorProtocol"
        )

    def test_read_returns_required_fields(self):
        sensor = MockSensor(value=42.0, unit="m3/s")
        reading = sensor.read()
        assert "value" in reading
        assert "unit" in reading
        assert "timestamp" in reading
        assert "quality" in reading
        assert reading["value"] == 42.0

    def test_get_status_returns_required_fields(self):
        sensor = MockSensor()
        status = sensor.get_status()
        assert "online" in status
        assert "battery" in status
        assert "last_seen" in status
        assert "diagnostics" in status


class TestActuatorProtocolCompliance:
    """Verify MockActuator satisfies ActuatorProtocol."""

    def test_isinstance_check(self):
        act = MockActuator()
        assert isinstance(act, ActuatorProtocol), (
            "MockActuator must satisfy ActuatorProtocol"
        )

    def test_execute_returns_required_fields(self):
        act = MockActuator()
        result = act.execute({"action": "set_position", "value": 0.5})
        assert result["success"] is True
        assert "actual" in result
        assert "timestamp" in result

    def test_get_position_returns_required_fields(self):
        act = MockActuator()
        pos = act.get_position()
        assert "position" in pos
        assert "unit" in pos
        assert "mode" in pos


class TestDetectorProtocolCompliance:
    """Verify MockDetector satisfies DetectorProtocol."""

    def test_isinstance_check(self):
        det = MockDetector()
        assert isinstance(det, DetectorProtocol), (
            "MockDetector must satisfy DetectorProtocol"
        )

    def test_detect_returns_required_fields(self):
        det = MockDetector()
        result = det.detect({"pressure": [100, 99, 95, 80]})
        assert "detected" in result
        assert "score" in result
        assert "details" in result

    def test_localize_returns_required_fields(self):
        det = MockDetector()
        det.set_detected(True)
        detection = det.detect({"pressure": [80, 60]})
        loc = det.localize(detection)
        assert "location" in loc
        assert "confidence" in loc
        assert "candidates" in loc


class TestPredictorProtocolCompliance:
    """Verify MockPredictor satisfies PredictorProtocol."""

    def test_isinstance_check(self):
        pred = MockPredictor()
        assert isinstance(pred, PredictorProtocol), (
            "MockPredictor must satisfy PredictorProtocol"
        )

    def test_predict_returns_required_fields(self):
        pred = MockPredictor()
        result = pred.predict(data={"last_value": 5.0}, horizon=12.0)
        assert "forecast" in result
        assert "confidence" in result
        assert "metadata" in result
        assert len(result["forecast"]) == 12


class TestSchedulerProtocolCompliance:
    """Verify MockScheduler satisfies SchedulerProtocol."""

    def test_isinstance_check(self):
        sched = MockScheduler()
        assert isinstance(sched, SchedulerProtocol), (
            "MockScheduler must satisfy SchedulerProtocol"
        )

    def test_optimize_returns_required_fields(self):
        sched = MockScheduler()
        result = sched.optimize(
            network={"assets": ["pump_1", "pump_2"]},
            objectives={"cost": "minimize"},
            constraints={"max_flow": 100.0},
        )
        assert "schedule" in result
        assert "objective_value" in result
        assert "feasible" in result
        assert result["feasible"] is True


class TestDigitalTwinProtocolCompliance:
    """Verify MockDigitalTwin satisfies DigitalTwinProtocol."""

    def test_isinstance_check(self):
        twin = MockDigitalTwin()
        assert isinstance(twin, DigitalTwinProtocol), (
            "MockDigitalTwin must satisfy DigitalTwinProtocol"
        )

    def test_sync_predict_cycle(self):
        twin = MockDigitalTwin()
        sync_result = twin.sync({"level": 3.5, "flow": 10.0})
        assert sync_result["synced"] is True
        assert "drift" in sync_result

        pred = twin.predict(duration=3600.0)
        assert "states" in pred
        assert "confidence" in pred
        assert pred["confidence"] > 0.5  # should be high after sync

    def test_get_discrepancy_returns_required_fields(self):
        twin = MockDigitalTwin()
        twin.sync({"level": 3.0})
        disc = twin.get_discrepancy()
        assert "variables" in disc
        assert "overall" in disc
        assert "timestamp" in disc


class TestScadaProtocolCompliance:
    """Verify MockScada satisfies ScadaProtocol."""

    def test_isinstance_check(self):
        scada = MockScada()
        assert isinstance(scada, ScadaProtocol), (
            "MockScada must satisfy ScadaProtocol"
        )

    def test_connect_read_write_disconnect_cycle(self):
        scada = MockScada()
        assert scada.connect({"host": "localhost", "port": 502}) is True
        scada.set_point("water_level", 3.5)

        readings = scada.read_points(["water_level", "nonexistent"])
        assert readings["water_level"]["value"] == 3.5
        assert readings["water_level"]["quality"] == "good"
        assert readings["nonexistent"]["quality"] == "bad"

        assert scada.write_point("flow", 10.0) is True
        scada.disconnect()
        assert scada.write_point("flow", 20.0) is False


# ============================================================================
# 2. Role Module Registration Tests
# ============================================================================


# Role modules and their expected locations
ROLE_MODULES = {
    "HydroGuard": ("hydroguard.role", "OperatorRoleModule"),
    "HydroDesign": ("hydrodesign.role", "DesignerRoleModule"),
    "HydroArena": ("hydroarena.role", "ContestRoleModule"),
    "HydroEdu.educator": ("hydroedu.role", "EducatorRoleModule"),
    "HydroEdu.student": ("hydroedu.role", "StudentRoleModule"),
    "HydroLab": ("hydrolab.role", "ResearcherRoleModule"),
}


class TestRoleModuleInterfaces:
    """Test that each project's role module exposes the expected interface."""

    @pytest.fixture(params=list(ROLE_MODULES.keys()))
    def role_instance(self, request):
        """Attempt to import and instantiate each role module."""
        project = request.param
        module_path, class_name = ROLE_MODULES[project]
        project_base = project.split(".")[0]
        if not PROJECTS.get(project_base, Path(".")).exists():
            pytest.skip(f"{project_base} project directory not found")
        try:
            mod = importlib.import_module(module_path)
        except ImportError as exc:
            pytest.skip(f"Cannot import {module_path}: {exc}")
        cls = getattr(mod, class_name, None)
        if cls is None:
            pytest.fail(f"{class_name} not found in {module_path}")
        return cls(), project

    def test_has_role_identifier(self, role_instance):
        """Every role module must expose a role identifier.

        This can be via get_role_id() method or a 'name' attribute
        (HydroGuard's OperatorRoleModule uses a dataclass name field).
        """
        instance, project = role_instance
        if hasattr(instance, "get_role_id"):
            role_id = instance.get_role_id()
        elif hasattr(instance, "name"):
            role_id = instance.name
        else:
            pytest.fail(f"{project} role module has neither get_role_id() nor name")
        assert isinstance(role_id, str) and len(role_id) > 0

    def test_has_skill_listing(self, role_instance):
        """Role modules should expose skills via get_skills() or get_config()."""
        instance, project = role_instance
        if hasattr(instance, "get_skills"):
            skills = instance.get_skills()
            assert isinstance(skills, list), (
                f"{project}: get_skills() must return a list"
            )
        elif hasattr(instance, "get_config"):
            config = instance.get_config()
            assert hasattr(config, "skills"), (
                f"{project}: get_config().skills must exist"
            )
        else:
            # HydroGuard OperatorRoleModule uses get_tools() instead
            assert hasattr(instance, "get_tools") or hasattr(instance, "capabilities"), (
                f"{project}: role module must have get_skills(), get_config(), "
                f"or get_tools()"
            )

    def test_has_mcp_tools_listing(self, role_instance):
        """Role modules should list their MCP tools."""
        instance, project = role_instance
        if hasattr(instance, "get_mcp_tools"):
            tools = instance.get_mcp_tools()
            assert isinstance(tools, list)
        elif hasattr(instance, "get_config"):
            config = instance.get_config()
            assert hasattr(config, "mcp_tools")
        elif hasattr(instance, "get_tools"):
            tools = instance.get_tools()
            assert isinstance(tools, list)
        else:
            pytest.skip(f"{project}: no MCP tools listing method found")

    def test_role_id_is_unique_and_descriptive(self, role_instance):
        """Role IDs should be meaningful identifiers."""
        instance, _ = role_instance
        if hasattr(instance, "get_role_id"):
            role_id = instance.get_role_id()
        elif hasattr(instance, "name"):
            role_id = instance.name
        else:
            pytest.fail("No role identifier found")
        expected_ids = {
            "operator", "designer", "contest", "educator", "student", "researcher"
        }
        assert role_id in expected_ids, (
            f"Unexpected role_id '{role_id}'; expected one of {expected_ids}"
        )


# ============================================================================
# 3. MCP Server Tool Schema Tests
# ============================================================================


class TestMCPToolSchemas:
    """Test that MCP tool definitions have proper schemas."""

    def _get_guard_tools(self) -> list[dict]:
        """Get tools from HydroGuard's OperatorRoleModule."""
        try:
            from hydroguard.role import OperatorRoleModule
            return OperatorRoleModule().get_tools()
        except ImportError:
            pytest.skip("HydroGuard not importable")

    def test_guard_tools_have_required_fields(self):
        """Each tool must have name, description, and inputSchema."""
        tools = self._get_guard_tools()
        assert len(tools) > 0, "OperatorRoleModule should expose at least one tool"
        for tool in tools:
            assert "name" in tool, f"Tool missing 'name': {tool}"
            assert "description" in tool, f"Tool {tool.get('name')} missing 'description'"
            assert "inputSchema" in tool, f"Tool {tool.get('name')} missing 'inputSchema'"

    def test_guard_tool_names_are_namespaced(self):
        """Tool names should be dot-namespaced (e.g. 'station.collect_data')."""
        tools = self._get_guard_tools()
        for tool in tools:
            name = tool["name"]
            assert "." in name, (
                f"Tool name '{name}' should be dot-namespaced (e.g. 'domain.action')"
            )

    def test_guard_tool_input_schemas_are_valid_json_schema(self):
        """inputSchema should be a valid JSON Schema object."""
        tools = self._get_guard_tools()
        for tool in tools:
            schema = tool["inputSchema"]
            assert isinstance(schema, dict), (
                f"inputSchema for '{tool['name']}' must be a dict"
            )
            assert schema.get("type") == "object", (
                f"inputSchema for '{tool['name']}' must have type=object"
            )
            assert "properties" in schema, (
                f"inputSchema for '{tool['name']}' must have 'properties'"
            )

    def test_guard_tool_required_fields_reference_existing_properties(self):
        """Required fields in inputSchema must reference defined properties."""
        tools = self._get_guard_tools()
        for tool in tools:
            schema = tool["inputSchema"]
            required = schema.get("required", [])
            properties = schema.get("properties", {})
            for req_field in required:
                assert req_field in properties, (
                    f"Tool '{tool['name']}' requires '{req_field}' but it is "
                    f"not defined in properties"
                )

    def test_satellite_role_mcp_tools_are_strings(self):
        """Satellite projects list MCP tool names as strings."""
        role_specs = [
            ("hydrodesign.role", "DesignerRoleModule"),
            ("hydroarena.role", "ContestRoleModule"),
            ("hydroedu.role", "EducatorRoleModule"),
            ("hydrolab.role", "ResearcherRoleModule"),
        ]
        for module_path, class_name in role_specs:
            try:
                mod = importlib.import_module(module_path)
                cls = getattr(mod, class_name)
                instance = cls()
            except (ImportError, AttributeError):
                continue

            if hasattr(instance, "get_mcp_tools"):
                tools = instance.get_mcp_tools()
                assert isinstance(tools, list)
                for t in tools:
                    assert isinstance(t, str), (
                        f"{class_name}.get_mcp_tools() items must be strings, "
                        f"got {type(t)}"
                    )
            elif hasattr(instance, "get_config"):
                config = instance.get_config()
                for t in config.mcp_tools:
                    assert isinstance(t, str)


# ============================================================================
# 4. Mock Compatibility Tests
# ============================================================================


class TestMockDropInCompatibility:
    """Test that contract mocks can be used as drop-in replacements.

    These tests simulate real usage patterns where a test would inject a
    mock in place of a real implementation.
    """

    def test_mock_simulator_in_control_loop(self):
        """MockSimulator + MockController can run a simulated control loop."""
        sim = MockSimulator()
        ctrl = MockController()

        sim.set_boundary({"inflow": 10.0})
        result = sim.simulate(params={"roughness": 0.013}, duration=300.0, dt=10.0)
        state = sim.get_state()

        action = ctrl.compute_action(
            state=state,
            target={"level": 3.0},
            constraints={"max_gate": 1.0},
        )
        assert "actions" in action

    def test_mock_sensor_feeds_predictor(self):
        """MockSensor readings can be fed into MockPredictor."""
        sensor = MockSensor(value=5.0, unit="m")
        pred = MockPredictor()

        reading = sensor.read()
        forecast = pred.predict(
            data={"last_value": reading["value"]},
            horizon=6.0,
        )
        assert len(forecast["forecast"]) == 6
        assert all(v == 5.0 for v in forecast["forecast"])

    def test_mock_detector_with_mock_sensor(self):
        """MockDetector can process MockSensor readings."""
        sensor = MockSensor(value=100.0, unit="kPa")
        det = MockDetector()

        det.set_detected(True, score=0.98)
        reading = sensor.read()
        detection = det.detect({"pressure": reading["value"]})
        assert detection["detected"] is True
        assert detection["score"] == 0.98

        location = det.localize(detection)
        assert location["confidence"] > 0

    def test_mock_scada_with_mock_actuator(self):
        """MockScada and MockActuator can be used together."""
        scada = MockScada()
        actuator = MockActuator(position=0.0, unit="fraction")

        scada.connect({"host": "127.0.0.1"})
        scada.set_point("gate_1_setpoint", 0.75)

        readings = scada.read_points(["gate_1_setpoint"])
        setpoint = readings["gate_1_setpoint"]["value"]

        result = actuator.execute({"action": "set_position", "value": setpoint})
        assert result["success"] is True
        assert result["actual"] == 0.75

        pos = actuator.get_position()
        assert pos["position"] == 0.75

    def test_mock_digital_twin_full_cycle(self):
        """MockDigitalTwin can run sync-predict-discrepancy cycle."""
        twin = MockDigitalTwin()
        sensor = MockSensor(value=3.5, unit="m")

        reading = sensor.read()
        sync = twin.sync({"level": reading["value"]})
        assert sync["synced"] is True

        prediction = twin.predict(duration=1800.0)
        assert len(prediction["states"]) > 0
        assert prediction["confidence"] > 0.8  # high after sync

        disc = twin.get_discrepancy()
        assert disc["overall"] >= 0

    def test_mock_scheduler_round_trip(self):
        """MockScheduler can optimize and return feasible schedule."""
        sched = MockScheduler()
        result = sched.optimize(
            network={"assets": ["pump_A", "pump_B", "gate_C"]},
            objectives={"cost": "minimize", "reliability": "maximize"},
            constraints={"max_total_flow": 50.0},
        )
        assert result["feasible"] is True
        assert "pump_A" in result["schedule"]
        assert "pump_B" in result["schedule"]
        assert "gate_C" in result["schedule"]

    def test_mock_mcp_client_register_and_call(self):
        """MockMCPClient supports register-then-call pattern."""
        client = MockMCPClient()
        client.register_response(
            "hydro-guard", "station.collect_data",
            {"status": "ok", "readings": {"level": 3.2}},
        )

        result = client.call_sync(
            "hydro-guard", "station.collect_data",
            {"station_id": "STN_001"},
        )
        assert result["status"] == "ok"
        assert result["readings"]["level"] == 3.2

    def test_mock_mcp_client_callable_response(self):
        """MockMCPClient supports callable responses for dynamic mocks."""
        client = MockMCPClient()
        client.register_response(
            "hydro-guard", "health.get_score",
            lambda params: {"score": 85, "equipment": params.get("equipment_id")},
        )

        result = client.call_sync(
            "hydro-guard", "health.get_score",
            {"equipment_id": "PUMP_001"},
        )
        assert result["score"] == 85
        assert result["equipment"] == "PUMP_001"

    def test_mock_mcp_client_default_response(self):
        """MockMCPClient returns a default response for unregistered tools."""
        client = MockMCPClient()
        result = client.call_sync("unknown-server", "unknown-tool", {})
        assert result["status"] == "mock"


# ============================================================================
# 5. Entry Points Configuration Tests
# ============================================================================


class TestEntryPointsConfiguration:
    """Validate that pyproject.toml entry_points are properly configured."""

    EXPECTED_ROLES = {
        "HydroGuard": {
            "entry_point_name": "operator",
            "target": "hydroguard.role:OperatorRoleModule",
        },
        "HydroDesign": {
            "entry_point_name": "designer",
            "target": "hydrodesign.role:DesignerRoleModule",
        },
        "HydroArena": {
            "entry_point_name": "contest",
            "target": "hydroarena.role:ContestRoleModule",
        },
        "HydroEdu_educator": {
            "entry_point_name": "educator",
            "target": "hydroedu.role:EducatorRoleModule",
        },
        "HydroEdu_student": {
            "entry_point_name": "student",
            "target": "hydroedu.role:StudentRoleModule",
        },
        "HydroLab": {
            "entry_point_name": "researcher",
            "target": "hydrolab.role:ResearcherRoleModule",
        },
    }

    @staticmethod
    def _parse_pyproject_entry_points(pyproject_path: Path) -> dict[str, dict[str, str]]:
        """Parse entry points from a pyproject.toml without toml library.

        Returns a dict: {group_name: {ep_name: ep_target}}.
        """
        if not pyproject_path.exists():
            return {}

        text = pyproject_path.read_text(encoding="utf-8")
        entry_points: dict[str, dict[str, str]] = {}

        # Simple parser for [project.entry-points."group"] sections
        import re

        pattern = r'\[project\.entry-points\."([^"]+)"\]\s*\n((?:[^\[].+\n)*)'
        for match in re.finditer(pattern, text):
            group = match.group(1)
            body = match.group(2)
            eps: dict[str, str] = {}
            for line in body.strip().splitlines():
                line = line.strip()
                if "=" in line:
                    k, v = line.split("=", 1)
                    eps[k.strip()] = v.strip().strip('"')
            entry_points[group] = eps

        return entry_points

    @pytest.mark.parametrize("project_key", list(EXPECTED_ROLES.keys()))
    def test_role_entry_point_exists(self, project_key):
        """Each satellite project must register a role entry point."""
        expected = self.EXPECTED_ROLES[project_key]
        project_dir_name = project_key.split("_")[0]
        pyproject = PROJECTS.get(project_dir_name)
        if pyproject is None:
            pyproject = Path(f"D:/research/{project_dir_name}")
        pyproject_path = pyproject / "pyproject.toml"

        if not pyproject_path.exists():
            pytest.skip(f"pyproject.toml not found for {project_dir_name}")

        eps = self._parse_pyproject_entry_points(pyproject_path)
        roles_group = eps.get("hydromind.roles", {})

        ep_name = expected["entry_point_name"]
        assert ep_name in roles_group, (
            f"Entry point '{ep_name}' not found in hydromind.roles group "
            f"of {pyproject_path}. Found: {list(roles_group.keys())}"
        )

    @pytest.mark.parametrize("project_key", list(EXPECTED_ROLES.keys()))
    def test_role_entry_point_target_importable(self, project_key):
        """The target of each role entry point must be importable."""
        expected = self.EXPECTED_ROLES[project_key]
        target = expected["target"]
        module_path, class_name = target.rsplit(":", 1)

        try:
            mod = importlib.import_module(module_path)
        except ImportError as exc:
            pytest.skip(f"Cannot import {module_path}: {exc}")

        cls = getattr(mod, class_name, None)
        assert cls is not None, (
            f"Class '{class_name}' not found in module '{module_path}'"
        )
        # Must be instantiable
        instance = cls()
        assert instance is not None

    def test_hydroguard_engine_entry_point(self):
        """HydroGuard should register an engine entry point."""
        pyproject = PROJECTS["HydroGuard"] / "pyproject.toml"
        if not pyproject.exists():
            pytest.skip("HydroGuard pyproject.toml not found")

        text = pyproject.read_text(encoding="utf-8")
        # Check that 'hydromind.engines' group exists and contains 'hydroguard'
        assert "hydromind.engines" in text, (
            "HydroGuard pyproject.toml should have hydromind.engines entry point group"
        )
        assert "hydroguard" in text, (
            "HydroGuard must register 'hydroguard' in hydromind.engines entry points"
        )


# ============================================================================
# 6. Cross-Project Consistency Tests
# ============================================================================


class TestCrossProjectConsistency:
    """Verify consistency across the ecosystem."""

    def test_all_project_directories_exist(self):
        """All expected satellite projects should have directories."""
        missing = [
            name for name, path in PROJECTS.items() if not path.exists()
        ]
        if missing:
            pytest.skip(
                "Cross-project consistency checks require a full HydroMind "
                f"workspace. Missing project directories: {missing}"
            )

    def test_all_projects_have_pyproject_toml(self):
        """Every project must have a pyproject.toml."""
        missing = []
        for name, path in PROJECTS.items():
            if path.exists() and not (path / "pyproject.toml").exists():
                missing.append(name)
        assert len(missing) == 0, f"Projects missing pyproject.toml: {missing}"

    def test_all_projects_depend_on_contracts(self):
        """Satellite projects should depend on hydromind-contracts."""
        for name, path in PROJECTS.items():
            pyproject = path / "pyproject.toml"
            if not pyproject.exists():
                continue
            text = pyproject.read_text(encoding="utf-8")
            has_dep = (
                "hydromind-contracts" in text
                or "hydromind_contracts" in text
            )
            assert has_dep, (
                f"{name} should depend on hydromind-contracts "
                f"(in dependencies or optional-dependencies)"
            )

    def test_role_ids_are_unique(self):
        """No two projects should register the same role_id."""
        role_ids: dict[str, str] = {}
        for project, (module_path, class_name) in ROLE_MODULES.items():
            try:
                mod = importlib.import_module(module_path)
                cls = getattr(mod, class_name)
                instance = cls()
                rid = instance.get_role_id() if hasattr(instance, "get_role_id") else getattr(instance, "name", None)
                if rid in role_ids:
                    pytest.fail(
                        f"Duplicate role_id '{rid}' registered by "
                        f"'{project}' and '{role_ids[rid]}'"
                    )
                role_ids[rid] = project
            except (ImportError, AttributeError):
                continue

        if not role_ids:
            pytest.skip(
                "Role uniqueness check requires importable satellite role modules "
                "from a full HydroMind workspace."
            )
