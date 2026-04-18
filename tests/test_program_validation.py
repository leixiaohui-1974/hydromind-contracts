import json
import sys

import pytest

from hydromind_contracts.cli import main as contracts_main
from hydromind_contracts.program_validation import (
    validate_agent_network,
    validate_agent_node_profile,
    validate_agent_profile,
    validate_agent_skill_binding,
    validate_capability_mcp_server,
    validate_boundary_condition_set,
    validate_case_manifest,
    validate_distributed_task_receipt,
    validate_dispatch_topology,
    validate_execution_lane,
    validate_execution_provider,
    validate_final_report,
    validate_fallback_policy,
    validate_gateway_mcp_route,
    validate_host_session_binding,
    validate_hourly_schedule_result,
    validate_lifecycle_phase,
    validate_management_level,
    validate_model_capability_matrix,
    validate_model_delivery,
    validate_model_eval_summary,
    validate_model_registry_entry,
    validate_model_routing_policy,
    validate_model_selection_trace,
    validate_stage_metric_summary,
    validate_platform_capability,
    validate_readiness_board,
    validate_release_manifest,
    validate_review_bundle,
    validate_role_profile,
    validate_role_reasoning_scaffold,
    validate_session_mode,
    validate_skill_manifest,
    validate_skill_execution_policy,
    validate_target_volume_objective,
    validate_team_run_state,
    validate_tier_message,
    validate_time_window_constraint,
    validate_tool_invocation_trace,
    validate_mcp_invocation_policy,
    validate_runtime_telemetry_record,
    validate_workflow_business_review,
    validate_algorithm_benchmark_record,
    validate_workflow_report_section,
    validate_workflow_run,
)


def _sample_workflow_run(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "WorkflowRun",
        "case_id": "demo",
        "workflow_name": "model",
        "canonical_workflow_key": "model_entry",
        "run_id": "session-1:model",
        "status": "completed",
        "inputs": {
            "session_id": "session-1",
            "profile": "smart",
        },
        "outputs": {
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
        },
        "contracts_emitted": ["WorkflowRun"],
        "artifacts_emitted": [],
        "started_at": "2026-04-15T00:00:00Z",
        "finished_at": "2026-04-15T00:01:00Z",
        "trace_id": "session-1:model:trace",
        "trace_summary": {},
    }
    payload.update(overrides)
    return payload


def _sample_team_run_state(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "TeamRunState",
        "session_id": "session-1",
        "case_id": "demo",
        "status": "planned",
        "started_at": "2026-04-15T00:00:00Z",
        "updated_at": "2026-04-15T00:00:00Z",
        "profile": "smart",
        "role_id": "designer",
        "recommended_workflows": ["model", "report"],
    }
    payload.update(overrides)
    return payload


def _sample_lifecycle_phase(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "LifecyclePhase",
        "lifecycle_stage_id": "operations",
        "display_name": "运行",
        "mission": "realtime_dispatch_and_control",
        "outputs": ["dispatch_plan_report", "decision_trace_report"],
    }
    payload.update(overrides)
    return payload


def _sample_management_level(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ManagementLevel",
        "management_level_id": "center",
        "display_name": "中心",
        "scope": "full_line",
        "responsibilities": ["four_forecasts", "dispatch_policy"],
    }
    payload.update(overrides)
    return payload


def _sample_role_profile(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "RoleProfile",
        "role_profile_id": "operations_dispatcher",
        "display_name": "调度运行智能体",
        "lifecycle_stage_id": "operations",
        "default_management_level_id": "center",
        "workflow_focus": ["realtime_assimilation", "dispatch_control"],
    }
    payload.update(overrides)
    return payload


def _sample_agent_node_profile(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "AgentNodeProfile",
        "agent_node_profile_id": "center_dispatch_commander",
        "display_name": "中心调度指挥智能体",
        "lifecycle_stage_id": "operations",
        "management_level_id": "center",
        "role_profile_id": "operations_dispatcher",
        "scope_pattern": "full_line",
    }
    payload.update(overrides)
    return payload


def _sample_session_mode(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "SessionMode",
        "agent_session_mode_id": "supervised",
        "display_name": "人机协同",
        "human_interaction": "approve_or_adjust",
    }
    payload.update(overrides)
    return payload


def _sample_agent_profile(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "AgentProfile",
        "agent_profile_id": "center_dispatch_commander_agent",
        "display_name": "中心调度指挥智能体",
        "role_id": "operator",
        "role_profile_id": "operations_dispatcher",
        "lifecycle_stage_id": "operations",
        "management_level_id": "center",
        "default_session_mode_id": "supervised",
        "supported_skill_ids": ["dispatch_workshop_skill", "four_forecasts_skill"],
    }
    payload.update(overrides)
    return payload


def _sample_skill_manifest(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "SkillManifest",
        "skill_id": "dispatch_workshop_skill",
        "display_name": "Dispatch Workshop Skill",
        "category": "workflow_bundle",
        "lifecycle_stage_ids": ["operations"],
        "workflow_keys": ["state_est", "ensemble_forecast", "autonomy_autorun"],
        "canonical_workflow_keys": ["state_estimation", "ensemble_forecast", "autonomous_operation"],
        "entry_command": "hydromind case-dispatch-workshop --case-id <case-id> --json",
    }
    payload.update(overrides)
    return payload


def _sample_agent_skill_binding(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "AgentSkillBinding",
        "binding_id": "center_dispatch_commander_agent:dispatch_workshop_skill",
        "agent_profile_id": "center_dispatch_commander_agent",
        "skill_id": "dispatch_workshop_skill",
        "activation_mode": "default",
    }
    payload.update(overrides)
    return payload


def _sample_role_reasoning_scaffold(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "RoleReasoningScaffold",
        "scaffold_id": "operations_dispatcher_default",
        "role_id": "operator",
        "lifecycle_stage_ids": ["operations"],
        "goal_types": ["dispatch_decision"],
        "required_context_slots": ["case_context", "role_context"],
        "decision_steps": ["confirm_runtime_auth", "review_forecast"],
        "required_evidence": ["runtime_auth", "four_forecasts"],
        "forbidden_shortcuts": ["skip_runtime_auth_check"],
        "handoff_rules": ["regional_to_central_takeover"],
    }
    payload.update(overrides)
    return payload


def _sample_skill_execution_policy(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "SkillExecutionPolicy",
        "policy_id": "dispatch_workshop_skill",
        "skill_id": "dispatch_workshop_skill",
        "entry_conditions": ["operations_case"],
        "required_inputs": ["case_id"],
        "execution_steps": ["inspect_case_agent_platform", "read_case_dispatch_workshop"],
        "preferred_mcp_sequence": ["runtime_auth_probe"],
        "fallback_steps": ["degrade_to_report_only_recommendation"],
        "quality_gates": ["approval_gate_checked"],
        "result_schema_expectation": ["dispatch_plan_report"],
    }
    payload.update(overrides)
    return payload


def _sample_mcp_invocation_policy(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "McpInvocationPolicy",
        "policy_id": "runtime_auth_probe_bundle",
        "mcp_group": "runtime_auth",
        "capability_server_ids": ["runtime_auth_capability_server"],
        "gateway_route_ids": ["runtime_auth_gateway"],
        "supported_tasks": ["runtime_readiness"],
        "parameter_templates": {"case_id": "required"},
        "invocation_sequence": ["inspect_secret_backend", "inspect_auth_refs"],
        "retry_policy": "retry_once_on_timeout",
        "fallback_policy": "degrade_to_partial_readiness",
        "trace_requirements": ["tool_name", "status"],
    }
    payload.update(overrides)
    return payload


def _sample_capability_mcp_server(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "CapabilityMcpServer",
        "server_id": "runtime_auth_capability_server",
        "display_name": "Runtime Auth Capability Server",
        "server_kind": "capability_mcp",
        "transport": "inprocess_registry",
        "tool_ids": ["inspect_secret_backend", "execute_connector_probe"],
        "supported_task_types": ["runtime_readiness"],
    }
    payload.update(overrides)
    return payload


def _sample_gateway_mcp_route(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "GatewayMcpRoute",
        "route_id": "runtime_auth_gateway",
        "display_name": "Runtime Auth Product Gateway",
        "gateway_kind": "product_gateway_mcp",
        "entrypoint": "hydromind case-runtime-auth --case-id <case-id> --json",
        "capability_server_ids": ["runtime_auth_capability_server"],
        "supported_workflows": ["verify"],
        "supported_canonical_workflow_keys": ["runtime_verification"],
        "invocation_mode": "sync_cli",
    }
    payload.update(overrides)
    return payload


def _sample_tool_invocation_trace(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ToolInvocationTrace",
        "trace_id": "demo:runtime-auth:1",
        "case_id": "demo",
        "route_id": "runtime_auth_gateway",
        "server_id": "runtime_auth_capability_server",
        "tool_name": "inspect_secret_backend",
        "status": "completed",
        "recorded_at": "2026-04-17T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def _sample_execution_lane(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ExecutionLane",
        "lane_id": "model_core_internal_python_lane",
        "display_name": "Model Core Internal Python Lane",
        "provider_id": "hydromind-model-core",
        "adapter_type": "internal_python",
        "supported_workflows": ["state_est", "ensemble_forecast", "autonomy_assess", "autonomy_autorun"],
        "supported_canonical_workflow_keys": ["state_estimation", "ensemble_forecast", "autonomy_evaluation", "autonomous_operation"],
        "runtime_class": "native_python_worker",
        "dispatch_mode": "sync_local",
        "artifact_root_kind": "native_runtime_session_dir",
        "status": "active",
    }
    payload.update(overrides)
    return payload


def _sample_fallback_policy(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "FallbackPolicy",
        "fallback_policy_id": "operations_runtime_default",
        "display_name": "Operations Runtime Default Fallback",
        "supported_workflows": ["state_est", "ensemble_forecast", "autonomy_assess", "autonomy_autorun", "verify"],
        "supported_canonical_workflow_keys": ["state_estimation", "ensemble_forecast", "autonomy_evaluation", "autonomous_operation", "runtime_verification"],
        "primary_lane_id": "model_core_internal_python_lane",
        "fallback_lane_ids": ["hydrology_smart_cli_lane", "case_contract_reader_lane"],
        "degrade_mode": "fallback_then_degrade_to_case_contract_reader",
        "retry_budget": 1,
        "terminal_conditions": ["primary_lane_missing", "runtime_failure"],
    }
    payload.update(overrides)
    return payload


def _sample_distributed_task_receipt(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "DistributedTaskReceipt",
        "receipt_id": "session-1:state_est:receipt",
        "session_id": "session-1",
        "case_id": "demo",
        "workflow_name": "state_est",
        "canonical_workflow_key": "state_estimation",
        "lane_id": "model_core_internal_python_lane",
        "fallback_policy_id": "operations_runtime_default",
        "provider_id": "hydromind-model-core",
        "adapter_type": "internal_python",
        "status": "completed",
        "started_at": "2026-04-18T00:00:00Z",
        "finished_at": "2026-04-18T00:01:00Z",
        "artifact_refs": ["contracts/native_runtime/session-1/state_est"],
    }
    payload.update(overrides)
    return payload


def _sample_model_selection_trace(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ModelSelectionTrace",
        "selection_trace_id": "session-1:state_est:model-selection",
        "session_id": "session-1",
        "case_id": "demo",
        "workflow_name": "state_est",
        "canonical_workflow_key": "state_estimation",
        "role_id": "operator",
        "lifecycle_stage_id": "operations",
        "policy_id": "operations_runtime_default",
        "preferred_model_id": "hydromind_flow_control_ops",
        "fallback_model_ids": ["hydromind_model_core_primary"],
        "required_model_capability_tags": ["ops", "governance"],
        "eval_summary_ids": ["operations_runtime_default_eval"],
        "status": "resolved",
        "recorded_at": "2026-04-18T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def _sample_runtime_telemetry_record(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "RuntimeTelemetryRecord",
        "telemetry_id": "session-1:state_est:telemetry",
        "session_id": "session-1",
        "case_id": "demo",
        "workflow_name": "state_est",
        "canonical_workflow_key": "state_estimation",
        "status": "completed",
        "selection_trace_id": "session-1:state_est:model-selection",
        "model_policy_id": "operations_runtime_default",
        "preferred_model_id": "hydromind_flow_control_ops",
        "route_ids": ["runtime_auth_gateway"],
        "server_ids": ["runtime_auth_capability_server"],
        "lane_id": "model_core_internal_python_lane",
        "fallback_policy_id": "operations_runtime_default",
        "distributed_task_receipt_id": "session-1:state_est:receipt",
        "tool_trace_ids": ["demo:runtime-auth:1"],
        "artifact_refs": ["contracts/native_runtime/session-1/state_est"],
        "started_at": "2026-04-18T00:00:00Z",
        "finished_at": "2026-04-18T00:01:00Z",
    }
    payload.update(overrides)
    return payload


def _sample_stage_metric_summary(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "StageMetricSummary",
        "metric_summary_id": "demo:modeling_simulation:metrics",
        "case_id": "demo",
        "stage_id": "modeling_simulation",
        "metric_dimensions": ["hydrology_simulation_accuracy", "hydrodynamic_simulation_accuracy"],
        "covered_dimension_ids": [],
        "review_required_dimension_ids": ["hydrology_simulation_accuracy", "hydrodynamic_simulation_accuracy"],
        "evidence_missing_dimension_ids": [],
        "status": "review_required",
        "recorded_at": "2026-04-18T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def _sample_workflow_business_review(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "WorkflowBusinessReview",
        "workflow_review_id": "demo:modeling_simulation:hyd_sim:review",
        "case_id": "demo",
        "stage_id": "modeling_simulation",
        "workflow_name": "hyd_sim",
        "provider_id": "hydromind-model-core",
        "adapter_type": "internal_python",
        "lane_id": "model_core_internal_python_lane",
        "fallback_policy_id": "model_core_runtime_default",
        "artifact_refs": ["contracts/outcomes/hyd_sim.latest.json"],
        "status": "review_required",
        "review_questions": ["该 workflow 是否写回了水文模拟精度指标？"],
        "recorded_at": "2026-04-18T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def _sample_algorithm_benchmark_record(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "AlgorithmBenchmarkRecord",
        "benchmark_record_id": "demo:hyd_sim:benchmark",
        "case_id": "demo",
        "workflow_name": "hyd_sim",
        "algorithm_surface_id": "hydromind-model-core:internal_python:native_python_worker",
        "provider_id": "hydromind-model-core",
        "adapter_type": "internal_python",
        "runtime_class": "native_python_worker",
        "lane_id": "model_core_internal_python_lane",
        "fallback_policy_id": "model_core_runtime_default",
        "artifact_refs": ["contracts/outcomes/hyd_sim.latest.json"],
        "status": "review_required",
        "benchmark_dimensions": ["accuracy", "robustness", "failure_taxonomy"],
        "recorded_at": "2026-04-18T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def _sample_model_delivery(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ModelDelivery",
        "delivery_id": "demo:research-to-ops:v1",
        "case_id": "demo",
        "lifecycle_stage_id": "research_support",
        "producer_role_profile_id": "research_support_modeler",
        "consumer_lifecycle_stage_id": "operations",
        "deliverable_kind": "operations_support_package",
        "status": "ready",
        "artifact_refs": ["contracts/model_support_package.json"],
        "report_section_refs": ["operations_support_report"],
    }
    payload.update(overrides)
    return payload


def _sample_model_registry_entry(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ModelRegistryEntry",
        "model_id": "hydromind_model_core_primary",
        "provider_id": "hydromind-model-core",
        "display_name": "HydroMind Model Core Primary",
        "model_family": "hydro_model",
        "deployment_modes": ["internal_python"],
        "capability_tags": ["modeling", "report"],
        "supported_workflows": ["state_est", "report"],
        "status": "active",
    }
    payload.update(overrides)
    return payload


def _sample_model_capability_matrix(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ModelCapabilityMatrix",
        "matrix_id": "hydromind_model_core_primary_default",
        "model_id": "hydromind_model_core_primary",
        "workflow_capabilities": ["state_est", "report"],
        "skill_capabilities": ["dispatch_workshop_skill"],
        "risk_notes": ["not_for_direct_control_command_emission"],
        "quality_tier": "stable",
    }
    payload.update(overrides)
    return payload


def _sample_model_routing_policy(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ModelRoutingPolicy",
        "policy_id": "operations_runtime_default",
        "role_ids": ["operator"],
        "lifecycle_stage_ids": ["operations"],
        "preferred_model_id": "hydromind_flow_control_ops",
        "fallback_model_ids": ["hydromind_control_verification_guard"],
        "selection_rules": ["prefer_realtime_control_capability"],
        "required_capability_tags": ["scheduling", "verification"],
    }
    payload.update(overrides)
    return payload


def _sample_model_eval_summary(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "ModelEvalSummary",
        "eval_id": "operations_runtime_default_eval",
        "model_id": "hydromind_flow_control_ops",
        "policy_id": "operations_runtime_default",
        "evaluation_scope": "operator_operations_runtime",
        "pass_rate": 0.89,
        "known_failure_modes": ["approval_state_missing"],
        "recommended_for": ["dispatch_runtime"],
    }
    payload.update(overrides)
    return payload


def _sample_workflow_report_section(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "WorkflowReportSection",
        "stage_id": "control",
        "chapter_id": "chapter_06",
        "display_name": "控制与自主运行",
        "report_sections": ["control_optimization_result"],
    }
    payload.update(overrides)
    return payload


def _sample_agent_network(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "AgentNetwork",
        "case_id": "demo",
        "network_id": "demo:agent-network:v1",
        "nodes": [
            {
                "node_id": "session-alpha",
                "session_id": "session-alpha",
                "management_level_id": "center",
                "required_actor_scope": "central",
            }
        ],
        "edges": [
            {
                "edge_id": "edge-1",
                "from_node_id": "session-alpha",
                "to_node_id": "session-alpha",
                "edge_type": "self_reference",
            }
        ],
    }
    payload.update(overrides)
    return payload


def _sample_tier_message(**overrides):
    payload = {
        "schema_version": "1",
        "contract_type": "TierMessage",
        "message_id": "session-alpha:event:1",
        "session_id": "session-alpha",
        "case_id": "demo",
        "message_type": "session_started",
        "from_scope": "central",
        "to_scope": "central",
        "event_type": "session_started",
        "recorded_at": "2026-04-17T00:00:00Z",
    }
    payload.update(overrides)
    return payload


def test_validate_case_manifest_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "CaseManifest",
        "case_id": "demo",
        "display_name": "Demo",
        "project_type": "canal",
    }
    assert validate_case_manifest(payload)["case_id"] == "demo"


def test_validate_lifecycle_phase_minimum():
    assert validate_lifecycle_phase(_sample_lifecycle_phase())["lifecycle_stage_id"] == "operations"


def test_validate_management_level_minimum():
    assert validate_management_level(_sample_management_level())["management_level_id"] == "center"


def test_validate_role_profile_minimum():
    assert validate_role_profile(_sample_role_profile())["role_profile_id"] == "operations_dispatcher"


def test_validate_agent_node_profile_minimum():
    assert validate_agent_node_profile(_sample_agent_node_profile())["agent_node_profile_id"] == "center_dispatch_commander"


def test_validate_session_mode_minimum():
    assert validate_session_mode(_sample_session_mode())["agent_session_mode_id"] == "supervised"


def test_validate_agent_profile_minimum():
    assert validate_agent_profile(_sample_agent_profile())["agent_profile_id"] == "center_dispatch_commander_agent"


def test_validate_skill_manifest_minimum():
    assert validate_skill_manifest(_sample_skill_manifest())["skill_id"] == "dispatch_workshop_skill"


def test_validate_skill_manifest_rejects_misaligned_canonical_workflow_keys():
    with pytest.raises(ValueError, match="canonical_workflow_keys must align 1:1 with SkillManifest workflow_keys"):
        validate_skill_manifest(
            _sample_skill_manifest(
                canonical_workflow_keys=["state_estimation"],
            )
        )


def test_validate_agent_skill_binding_minimum():
    assert validate_agent_skill_binding(_sample_agent_skill_binding())["binding_id"] == "center_dispatch_commander_agent:dispatch_workshop_skill"


def test_validate_role_reasoning_scaffold_minimum():
    assert validate_role_reasoning_scaffold(_sample_role_reasoning_scaffold())["scaffold_id"] == "operations_dispatcher_default"


def test_validate_skill_execution_policy_minimum():
    assert validate_skill_execution_policy(_sample_skill_execution_policy())["policy_id"] == "dispatch_workshop_skill"


def test_validate_mcp_invocation_policy_minimum():
    assert validate_mcp_invocation_policy(_sample_mcp_invocation_policy())["policy_id"] == "runtime_auth_probe_bundle"


def test_validate_mcp_invocation_policy_requires_dualization_fields():
    with pytest.raises(ValueError, match="McpInvocationPolicy missing required fields: capability_server_ids, gateway_route_ids"):
        validate_mcp_invocation_policy(
            {
                "schema_version": "1",
                "contract_type": "McpInvocationPolicy",
                "policy_id": "runtime_auth_probe_bundle",
                "mcp_group": "runtime_auth",
                "supported_tasks": ["runtime_readiness"],
                "parameter_templates": {"case_id": "required"},
                "invocation_sequence": ["inspect_secret_backend"],
                "retry_policy": "retry_once_on_timeout",
                "fallback_policy": "degrade_to_partial_readiness",
                "trace_requirements": ["tool_name"],
            }
        )


def test_validate_capability_mcp_server_minimum():
    assert validate_capability_mcp_server(_sample_capability_mcp_server())["server_id"] == "runtime_auth_capability_server"


def test_validate_gateway_mcp_route_minimum():
    assert validate_gateway_mcp_route(_sample_gateway_mcp_route())["route_id"] == "runtime_auth_gateway"


def test_validate_gateway_mcp_route_rejects_misaligned_supported_canonical_workflow_keys():
    with pytest.raises(ValueError, match="supported_canonical_workflow_keys must align 1:1 with GatewayMcpRoute supported_workflows"):
        validate_gateway_mcp_route(
            _sample_gateway_mcp_route(
                supported_canonical_workflow_keys=[],
            )
        )


def test_validate_tool_invocation_trace_minimum():
    assert validate_tool_invocation_trace(_sample_tool_invocation_trace())["trace_id"] == "demo:runtime-auth:1"


def test_validate_model_registry_entry_minimum():
    assert validate_model_registry_entry(_sample_model_registry_entry())["model_id"] == "hydromind_model_core_primary"


def test_validate_model_capability_matrix_minimum():
    assert validate_model_capability_matrix(_sample_model_capability_matrix())["matrix_id"] == "hydromind_model_core_primary_default"


def test_validate_model_routing_policy_minimum():
    assert validate_model_routing_policy(_sample_model_routing_policy())["policy_id"] == "operations_runtime_default"


def test_validate_model_eval_summary_minimum():
    assert validate_model_eval_summary(_sample_model_eval_summary())["eval_id"] == "operations_runtime_default_eval"


def test_validate_execution_lane_minimum():
    assert validate_execution_lane(_sample_execution_lane())["lane_id"] == "model_core_internal_python_lane"


def test_validate_fallback_policy_minimum():
    assert validate_fallback_policy(_sample_fallback_policy())["fallback_policy_id"] == "operations_runtime_default"


def test_validate_distributed_task_receipt_minimum():
    assert validate_distributed_task_receipt(_sample_distributed_task_receipt())["receipt_id"] == "session-1:state_est:receipt"


def test_validate_model_selection_trace_minimum():
    assert validate_model_selection_trace(_sample_model_selection_trace())["selection_trace_id"] == "session-1:state_est:model-selection"


def test_validate_runtime_telemetry_record_minimum():
    assert validate_runtime_telemetry_record(_sample_runtime_telemetry_record())["telemetry_id"] == "session-1:state_est:telemetry"


def test_validate_stage_metric_summary_minimum():
    assert validate_stage_metric_summary(_sample_stage_metric_summary())["metric_summary_id"] == "demo:modeling_simulation:metrics"


def test_validate_workflow_business_review_minimum():
    assert validate_workflow_business_review(_sample_workflow_business_review())["workflow_review_id"] == "demo:modeling_simulation:hyd_sim:review"


def test_validate_algorithm_benchmark_record_minimum():
    assert validate_algorithm_benchmark_record(_sample_algorithm_benchmark_record())["benchmark_record_id"] == "demo:hyd_sim:benchmark"


def test_validate_model_delivery_minimum():
    assert validate_model_delivery(_sample_model_delivery())["delivery_id"] == "demo:research-to-ops:v1"


def test_validate_workflow_report_section_minimum():
    assert validate_workflow_report_section(_sample_workflow_report_section())["chapter_id"] == "chapter_06"


def test_validate_workflow_report_section_rejects_invalid_report_sections():
    with pytest.raises(ValueError, match="WorkflowReportSection report_sections must be a list of non-empty strings"):
        validate_workflow_report_section(_sample_workflow_report_section(report_sections=["", "ok"]))


def test_validate_agent_network_minimum():
    assert validate_agent_network(_sample_agent_network())["network_id"] == "demo:agent-network:v1"


def test_validate_tier_message_minimum():
    assert validate_tier_message(_sample_tier_message())["message_id"] == "session-alpha:event:1"


def test_validate_agent_network_rejects_duplicate_node_ids():
    with pytest.raises(ValueError, match="AgentNetwork nodes\\[1\\]\\.node_id must be unique"):
        validate_agent_network(
            _sample_agent_network(
                nodes=[
                    {
                        "node_id": "session-alpha",
                        "session_id": "session-alpha",
                        "management_level_id": "center",
                        "required_actor_scope": "central",
                    },
                    {
                        "node_id": "session-alpha",
                        "session_id": "session-beta",
                        "management_level_id": "subcenter",
                        "required_actor_scope": "regional",
                    },
                ]
            )
        )


def test_validate_workflow_run_minimum():
    payload = _sample_workflow_run()
    assert validate_workflow_run(payload)["workflow_name"] == "model"


def test_validate_workflow_run_accepts_trace_pointer_without_trace_id():
    payload = _sample_workflow_run(
        trace_id=None,
        trace_pointer="session://session-1/workflow/model",
        outputs={
            "source": "inferred_session_terminal",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "provider_id": "legacy-smart-cli",
            "adapter_type": "delegated_legacy",
            "trace_id": "session-1:model:trace",
        },
    )
    payload.pop("trace_id")
    validated = validate_workflow_run(payload)
    assert validated["trace_pointer"] == "session://session-1/workflow/model"


def test_validate_workflow_run_rejects_missing_provenance():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
        }
    )
    with pytest.raises(ValueError, match="WorkflowRun outputs missing required fields: provider_id"):
        validate_workflow_run(payload)


def test_validate_workflow_run_rejects_missing_trace_link():
    payload = _sample_workflow_run(trace_id=None)
    payload.pop("trace_id")
    with pytest.raises(ValueError, match="WorkflowRun must include trace_id or trace_pointer"):
        validate_workflow_run(payload)


def test_validate_workflow_run_rejects_status_mismatch_with_terminal_status():
    payload = _sample_workflow_run(
        status="failed",
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
        },
    )
    with pytest.raises(ValueError, match="outputs.terminal_status must equal WorkflowRun status"):
        validate_workflow_run(payload)


def test_validate_workflow_run_rejects_output_trace_id_mismatch():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:other-trace",
        },
    )
    with pytest.raises(ValueError, match="outputs.trace_id must equal WorkflowRun trace_id"):
        validate_workflow_run(payload)


def test_validate_workflow_run_rejects_invalid_artifact_records():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {"run_summary": "contracts/model.run_summary.json"},
            "artifact_records": [{"artifact_id": "run_summary", "kind": "", "pointer": "contracts/model.run_summary.json"}],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
        },
    )
    with pytest.raises(ValueError, match="outputs.artifact_records\\[0\\].kind must be a non-empty string"):
        validate_workflow_run(payload)


def test_validate_workflow_run_rejects_unknown_artifact_kind():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {"run_summary": "contracts/model.run_summary.json"},
            "artifact_records": [{"artifact_id": "run_summary", "kind": "artifact.unknown", "pointer": "contracts/model.run_summary.json"}],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
        },
    )
    with pytest.raises(ValueError, match="outputs.artifact_records\\[0\\].kind must be one of:"):
        validate_workflow_run(payload)


def test_validate_workflow_run_rejects_artifacts_emitted_mismatch():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {"run_summary": "contracts/model.run_summary.json"},
            "artifact_records": [{"artifact_id": "run_summary", "kind": "runtime.run_summary", "pointer": "contracts/model.run_summary.json"}],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
        },
        artifacts_emitted=["wrong_id"],
    )
    with pytest.raises(ValueError, match="artifacts_emitted must equal WorkflowRun outputs.artifact_records artifact_id order"):
        validate_workflow_run(payload)


def test_validate_workflow_run_accepts_writeback_records():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
            "writeback_records": [
                {
                    "writeback_id": "session-1:intervention:abc",
                    "intervention_id": "session-1:intervention:abc",
                    "surface_id": "final_report_json",
                    "action": "report_edit",
                    "kind": "writeback.report",
                    "pointer": "contracts/final_report.v2.json",
                    "actor": "user",
                    "actor_scope": "regional",
                    "recorded_at": "2026-04-16T00:00:00Z",
                }
            ],
        },
    )
    validated = validate_workflow_run(payload)
    assert validated["outputs"]["writeback_records"][0]["kind"] == "writeback.report"


def test_validate_workflow_run_rejects_unknown_writeback_kind():
    payload = _sample_workflow_run(
        outputs={
            "source": "runtime",
            "terminal_status": "completed",
            "artifacts": {},
            "artifact_records": [],
            "provider_id": "hydromind-model-core",
            "adapter_type": "internal_python",
            "trace_id": "session-1:model:trace",
            "writeback_records": [
                {
                    "writeback_id": "session-1:intervention:abc",
                    "intervention_id": "session-1:intervention:abc",
                    "surface_id": "final_report_json",
                    "action": "report_edit",
                    "kind": "writeback.unknown",
                    "pointer": "contracts/final_report.v2.json",
                    "actor": "user",
                    "actor_scope": "regional",
                    "recorded_at": "2026-04-16T00:00:00Z",
                }
            ],
        },
    )
    with pytest.raises(ValueError, match="outputs.writeback_records\\[0\\].kind must be one of:"):
        validate_workflow_run(payload)


def test_validate_final_report_minimum():
    payload = {
        "meta": {},
        "case": {},
        "readiness": {},
        "review": {},
        "release": {},
        "quality": {},
        "recommendations": [],
    }
    assert validate_final_report(payload)["quality"] == {}


def test_validate_dispatch_topology_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "DispatchTopology",
        "case_id": "demo",
        "topology_id": "demo-topology",
        "network_type": "pump_pipe_tank",
        "corridors": [{"corridor_id": "corridor-1", "segment_count": 2}],
        "nodes": [{"node_id": "pump-1", "node_kind": "pump"}],
        "edges": [{"edge_id": "edge-1", "from_node": "pump-1", "to_node": "tank-1"}],
    }
    assert validate_dispatch_topology(payload)["network_type"] == "pump_pipe_tank"


def test_validate_target_volume_objective_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "TargetVolumeObjective",
        "case_id": "demo",
        "objective_id": "target-1",
        "objective_type": "delivery_volume",
        "target_volume_m3": 1500000,
        "horizon_hours": 24,
    }
    assert validate_target_volume_objective(payload)["horizon_hours"] == 24


def test_validate_time_window_constraint_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "TimeWindowConstraint",
        "case_id": "demo",
        "constraint_id": "window-1",
        "horizon_hours": 24,
        "allowed_periods": [1] * 24,
    }
    assert len(validate_time_window_constraint(payload)["allowed_periods"]) == 24


def test_validate_boundary_condition_set_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "BoundaryConditionSet",
        "case_id": "demo",
        "condition_set_id": "bc-1",
        "horizon_hours": 24,
        "boundary_conditions": [
            {"asset_id": "pump-1", "input_waterlevel_m": 4.2, "input_flow_m3s": 80.0},
        ],
    }
    assert validate_boundary_condition_set(payload)["condition_set_id"] == "bc-1"


def test_validate_hourly_schedule_result_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "HourlyScheduleResult",
        "case_id": "demo",
        "schedule_id": "schedule-1",
        "status": "sampled",
        "horizon_hours": 24,
        "objective_ref": "contracts/target_volume_objective.sample.json",
        "time_window_ref": "contracts/time_window_constraint.sample.json",
        "boundary_condition_ref": "contracts/boundary_condition_set.sample.json",
        "timeline": [{"hour_index": 0, "cost": 2.3}],
    }
    assert validate_hourly_schedule_result(payload)["status"] == "sampled"


def test_validate_readiness_board_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "ReadinessBoard",
        "cases": [{"case_id": "demo", "status": "ready"}],
    }
    assert validate_readiness_board(payload)["cases"][0]["status"] == "ready"


def test_validate_review_bundle_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "ReviewBundle",
        "case_id": "demo",
        "review_id": "review-1",
        "status": "pending",
    }
    assert validate_review_bundle(payload)["review_id"] == "review-1"


def test_validate_release_manifest_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "ReleaseManifest",
        "case_id": "demo",
        "release_id": "release-1",
        "status": "pending",
    }
    assert validate_release_manifest(payload)["release_id"] == "release-1"


def test_validate_platform_capability_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "PlatformCapability",
        "capability_id": "smart_run",
        "display_name": "Smart Run",
        "category": "runtime",
    }
    assert validate_platform_capability(payload)["capability_id"] == "smart_run"


def test_validate_execution_provider_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "ExecutionProvider",
        "provider_id": "hydromind-model-core",
        "display_name": "Model Core",
        "adapter_type": "internal_python",
        "capabilities": ["model", "report"],
    }
    assert validate_execution_provider(payload)["provider_id"] == "hydromind-model-core"


def test_validate_host_session_binding_minimum():
    payload = {
        "schema_version": "1",
        "contract_type": "HostSessionBinding",
        "binding_id": "hydrodesk.internal_ui",
        "platform_id": "hydrodesk",
        "entry_mode": "internal_ui",
        "supports_json": True,
        "supports_session": True,
    }
    assert validate_host_session_binding(payload)["binding_id"] == "hydrodesk.internal_ui"


def test_validate_team_run_state_minimum():
    payload = _sample_team_run_state()
    validated = validate_team_run_state(payload)
    assert validated["session_id"] == "session-1"
    assert validated["recommended_workflows"] == ["model", "report"]


def test_validate_team_run_state_allows_runtime_statuses():
    for status in [
        "planned",
        "running",
        "awaiting_human_review",
        "human_revision_requested",
        "approved_to_resume",
        "degraded",
        "blocked",
        "stopped",
        "completed",
        "failed",
    ]:
        payload = _sample_team_run_state(status=status, recommended_workflows=[])
        assert validate_team_run_state(payload)["status"] == status


def test_validate_team_run_state_rejects_unknown_status():
    payload = _sample_team_run_state(status="unknown")
    with pytest.raises(ValueError, match="TeamRunState status must be one of"):
        validate_team_run_state(payload)


def test_validate_team_run_state_validates_workflow_runs_shape():
    payload = _sample_team_run_state(
        status="completed",
        updated_at="2026-04-15T00:01:00Z",
        workflow_runs=[_sample_workflow_run()],
    )
    validated = validate_team_run_state(payload)
    assert validated["workflow_runs"][0]["workflow_name"] == "model"


def test_validate_team_run_state_validates_tool_invocation_traces_shape():
    payload = _sample_team_run_state(
        status="completed",
        updated_at="2026-04-15T00:01:00Z",
        tool_invocation_traces=[_sample_tool_invocation_trace(session_id="session-1", case_id="demo")],
    )
    validated = validate_team_run_state(payload)
    assert validated["tool_invocation_traces"][0]["trace_id"] == "demo:runtime-auth:1"


def test_validate_team_run_state_validates_distributed_task_receipts_shape():
    payload = _sample_team_run_state(
        status="completed",
        updated_at="2026-04-18T00:01:00Z",
        distributed_task_receipts=[_sample_distributed_task_receipt()],
    )
    validated = validate_team_run_state(payload)
    assert validated["distributed_task_receipts"][0]["lane_id"] == "model_core_internal_python_lane"


def test_validate_team_run_state_validates_model_selection_traces_shape():
    payload = _sample_team_run_state(
        status="planned",
        model_selection_traces=[_sample_model_selection_trace()],
    )
    validated = validate_team_run_state(payload)
    assert validated["model_selection_traces"][0]["policy_id"] == "operations_runtime_default"


def test_validate_team_run_state_validates_runtime_telemetry_records_shape():
    payload = _sample_team_run_state(
        status="completed",
        updated_at="2026-04-18T00:01:00Z",
        runtime_telemetry_records=[_sample_runtime_telemetry_record()],
    )
    validated = validate_team_run_state(payload)
    assert validated["runtime_telemetry_records"][0]["telemetry_id"] == "session-1:state_est:telemetry"


def test_validate_team_run_state_rejects_non_list_workflow_runs():
    payload = _sample_team_run_state(workflow_runs={})
    with pytest.raises(ValueError, match="TeamRunState workflow_runs must be a list"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_workflow_run_case_mismatch():
    payload = _sample_team_run_state(
        workflow_runs=[_sample_workflow_run(case_id="other-case")],
    )
    with pytest.raises(ValueError, match="workflow_runs case_id must match TeamRunState case_id"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_workflow_run_session_prefix_mismatch():
    payload = _sample_team_run_state(
        workflow_runs=[
            _sample_workflow_run(
                run_id="session-2:model",
                trace_id="session-2:model:trace",
                outputs={
                    "source": "runtime",
                    "terminal_status": "completed",
                    "artifacts": {},
                    "artifact_records": [],
                    "provider_id": "hydromind-model-core",
                    "adapter_type": "internal_python",
                    "trace_id": "session-2:model:trace",
                },
            )
        ],
    )
    with pytest.raises(ValueError, match="run_id must start with TeamRunState session_id"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_duplicate_workflow_run_ids():
    workflow_run = _sample_workflow_run()
    payload = _sample_team_run_state(workflow_runs=[workflow_run, dict(workflow_run)])
    with pytest.raises(ValueError, match="duplicate run_id"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_tool_invocation_trace_session_mismatch():
    payload = _sample_team_run_state(
        tool_invocation_traces=[_sample_tool_invocation_trace(session_id="session-2", case_id="demo")],
    )
    with pytest.raises(ValueError, match="tool_invocation_traces session_id must match TeamRunState session_id"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_distributed_task_receipt_session_mismatch():
    payload = _sample_team_run_state(
        distributed_task_receipts=[_sample_distributed_task_receipt(session_id="session-2")],
    )
    with pytest.raises(ValueError, match="distributed_task_receipts session_id must match TeamRunState session_id"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_model_selection_trace_session_mismatch():
    payload = _sample_team_run_state(
        model_selection_traces=[_sample_model_selection_trace(session_id="session-2")],
    )
    with pytest.raises(ValueError, match="model_selection_traces session_id must match TeamRunState session_id"):
        validate_team_run_state(payload)


def test_validate_team_run_state_rejects_runtime_telemetry_record_session_mismatch():
    payload = _sample_team_run_state(
        runtime_telemetry_records=[_sample_runtime_telemetry_record(session_id="session-2")],
    )
    with pytest.raises(ValueError, match="runtime_telemetry_records session_id must match TeamRunState session_id"):
        validate_team_run_state(payload)


def test_contracts_cli_list_contract_types_outputs_new_platform_types(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["hydromind-contracts", "list-contract-types"])
    contracts_main()
    payload = json.loads(capsys.readouterr().out)
    assert "PlatformCapability" in payload["contract_types"]
    assert "ExecutionProvider" in payload["contract_types"]
    assert "HostSessionBinding" in payload["contract_types"]
    assert "TeamRunState" in payload["contract_types"]
    assert "DispatchTopology" in payload["contract_types"]
    assert "TargetVolumeObjective" in payload["contract_types"]
    assert "TimeWindowConstraint" in payload["contract_types"]
    assert "BoundaryConditionSet" in payload["contract_types"]
    assert "HourlyScheduleResult" in payload["contract_types"]
    assert "LifecyclePhase" in payload["contract_types"]
    assert "ManagementLevel" in payload["contract_types"]
    assert "RoleProfile" in payload["contract_types"]
    assert "AgentNodeProfile" in payload["contract_types"]
    assert "SessionMode" in payload["contract_types"]
    assert "AgentProfile" in payload["contract_types"]
    assert "SkillManifest" in payload["contract_types"]
    assert "AgentSkillBinding" in payload["contract_types"]
    assert "RoleReasoningScaffold" in payload["contract_types"]
    assert "SkillExecutionPolicy" in payload["contract_types"]
    assert "McpInvocationPolicy" in payload["contract_types"]
    assert "CapabilityMcpServer" in payload["contract_types"]
    assert "GatewayMcpRoute" in payload["contract_types"]
    assert "ToolInvocationTrace" in payload["contract_types"]
    assert "ModelRegistryEntry" in payload["contract_types"]
    assert "ModelCapabilityMatrix" in payload["contract_types"]
    assert "ModelRoutingPolicy" in payload["contract_types"]
    assert "ModelEvalSummary" in payload["contract_types"]
    assert "ExecutionLane" in payload["contract_types"]
    assert "FallbackPolicy" in payload["contract_types"]
    assert "DistributedTaskReceipt" in payload["contract_types"]
    assert "ModelSelectionTrace" in payload["contract_types"]
    assert "RuntimeTelemetryRecord" in payload["contract_types"]
    assert "StageMetricSummary" in payload["contract_types"]
    assert "WorkflowBusinessReview" in payload["contract_types"]
    assert "AlgorithmBenchmarkRecord" in payload["contract_types"]
    assert "ModelDelivery" in payload["contract_types"]
    assert "WorkflowReportSection" in payload["contract_types"]
    assert "AgentNetwork" in payload["contract_types"]
    assert "TierMessage" in payload["contract_types"]


def test_contracts_cli_validate_contract_accepts_yaml(tmp_path, monkeypatch, capsys):
    payload = _sample_lifecycle_phase()
    target = tmp_path / "lifecycle_phase.yaml"
    target.write_text(
        "\n".join(
            [
                "schema_version: '1'",
                "contract_type: LifecyclePhase",
                "lifecycle_stage_id: operations",
                "display_name: 运行",
                "mission: realtime_dispatch_and_control",
                "outputs:",
                "  - dispatch_plan_report",
                "  - decision_trace_report",
            ]
        ),
        encoding="utf-8",
    )
    monkeypatch.setattr(sys, "argv", ["hydromind-contracts", "validate-contract", "LifecyclePhase", str(target)])
    contracts_main()
    output = json.loads(capsys.readouterr().out)
    assert output["status"] == "ok"
    assert output["contract_type"] == "LifecyclePhase"


def test_schema_files_exist_for_v5_platform_contracts():
    import pathlib

    root = pathlib.Path(__file__).resolve().parents[1] / "schemas"
    expected = {
        "lifecycle_phase.schema.json",
        "management_level.schema.json",
        "role_profile.schema.json",
        "agent_node_profile.schema.json",
        "session_mode.schema.json",
        "agent_profile.schema.json",
        "skill_manifest.schema.json",
        "agent_skill_binding.schema.json",
        "role_reasoning_scaffold.schema.json",
        "skill_execution_policy.schema.json",
        "mcp_invocation_policy.schema.json",
        "capability_mcp_server.schema.json",
        "gateway_mcp_route.schema.json",
        "tool_invocation_trace.schema.json",
        "execution_lane.schema.json",
        "fallback_policy.schema.json",
        "distributed_task_receipt.schema.json",
        "model_selection_trace.schema.json",
        "runtime_telemetry_record.schema.json",
        "stage_metric_summary.schema.json",
        "workflow_business_review.schema.json",
        "algorithm_benchmark_record.schema.json",
        "model_registry_entry.schema.json",
        "model_capability_matrix.schema.json",
        "model_routing_policy.schema.json",
        "model_eval_summary.schema.json",
        "model_delivery.schema.json",
        "workflow_report_section.schema.json",
        "agent_network.schema.json",
        "tier_message.schema.json",
    }
    assert expected.issubset({path.name for path in root.iterdir()})
