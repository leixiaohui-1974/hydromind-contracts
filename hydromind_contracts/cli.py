"""CLI for hydromind-contracts."""

from __future__ import annotations

import argparse
import json

from .program_validation import (
    validate_agent_network,
    validate_agent_node_profile,
    validate_agent_profile,
    validate_agent_skill_binding,
    validate_capability_mcp_server,
    validate_distributed_task_receipt,
    validate_execution_lane,
    validate_algorithm_benchmark_record,
    validate_mcp_invocation_policy,
    load_json_document,
    validate_lifecycle_phase,
    validate_management_level,
    validate_model_capability_matrix,
    validate_model_delivery,
    validate_model_eval_summary,
    validate_model_registry_entry,
    validate_model_routing_policy,
    validate_model_selection_trace,
    validate_boundary_condition_set,
    validate_case_manifest,
    validate_dispatch_topology,
    validate_fallback_policy,
    validate_execution_provider,
    validate_final_report,
    validate_host_session_binding,
    validate_hourly_schedule_result,
    validate_platform_capability,
    validate_readiness_board,
    validate_release_manifest,
    validate_review_bundle,
    validate_role_profile,
    validate_role_reasoning_scaffold,
    validate_session_mode,
    validate_skill_manifest,
    validate_skill_execution_policy,
    validate_gateway_mcp_route,
    validate_target_volume_objective,
    validate_team_run_state,
    validate_tier_message,
    validate_time_window_constraint,
    validate_tool_invocation_trace,
    validate_runtime_telemetry_record,
    validate_stage_metric_summary,
    validate_workflow_report_section,
    validate_workflow_business_review,
    validate_workflow_run,
)


VALIDATORS = {
    "CaseManifest": validate_case_manifest,
    "WorkflowRun": validate_workflow_run,
    "ReviewBundle": validate_review_bundle,
    "ReleaseManifest": validate_release_manifest,
    "FinalReport": validate_final_report,
    "DispatchTopology": validate_dispatch_topology,
    "TargetVolumeObjective": validate_target_volume_objective,
    "TimeWindowConstraint": validate_time_window_constraint,
    "BoundaryConditionSet": validate_boundary_condition_set,
    "HourlyScheduleResult": validate_hourly_schedule_result,
    "ReadinessBoard": validate_readiness_board,
    "PlatformCapability": validate_platform_capability,
    "ExecutionProvider": validate_execution_provider,
    "HostSessionBinding": validate_host_session_binding,
    "TeamRunState": validate_team_run_state,
    "LifecyclePhase": validate_lifecycle_phase,
    "ManagementLevel": validate_management_level,
    "RoleProfile": validate_role_profile,
    "AgentNodeProfile": validate_agent_node_profile,
    "SessionMode": validate_session_mode,
    "AgentProfile": validate_agent_profile,
    "SkillManifest": validate_skill_manifest,
    "AgentSkillBinding": validate_agent_skill_binding,
    "RoleReasoningScaffold": validate_role_reasoning_scaffold,
    "SkillExecutionPolicy": validate_skill_execution_policy,
    "McpInvocationPolicy": validate_mcp_invocation_policy,
    "CapabilityMcpServer": validate_capability_mcp_server,
    "GatewayMcpRoute": validate_gateway_mcp_route,
    "ToolInvocationTrace": validate_tool_invocation_trace,
    "ModelRegistryEntry": validate_model_registry_entry,
    "ModelCapabilityMatrix": validate_model_capability_matrix,
    "ModelRoutingPolicy": validate_model_routing_policy,
    "ModelEvalSummary": validate_model_eval_summary,
    "ExecutionLane": validate_execution_lane,
    "FallbackPolicy": validate_fallback_policy,
    "DistributedTaskReceipt": validate_distributed_task_receipt,
    "ModelSelectionTrace": validate_model_selection_trace,
    "RuntimeTelemetryRecord": validate_runtime_telemetry_record,
    "StageMetricSummary": validate_stage_metric_summary,
    "WorkflowBusinessReview": validate_workflow_business_review,
    "AlgorithmBenchmarkRecord": validate_algorithm_benchmark_record,
    "ModelDelivery": validate_model_delivery,
    "WorkflowReportSection": validate_workflow_report_section,
    "AgentNetwork": validate_agent_network,
    "TierMessage": validate_tier_message,
}


def cmd_list_contract_types(_args: argparse.Namespace) -> None:
    print(json.dumps({"contract_types": sorted(VALIDATORS.keys())}, ensure_ascii=False, indent=2))


def cmd_validate(args: argparse.Namespace) -> None:
    payload = load_json_document(args.path)
    validated = VALIDATORS[args.contract_type](payload)
    print(json.dumps({"status": "ok", "contract_type": args.contract_type, "validated_keys": sorted(validated.keys())}, ensure_ascii=False, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(prog="hydromind-contracts")
    sub = parser.add_subparsers(dest="command", required=True)

    list_parser = sub.add_parser("list-contract-types", help="List supported contract types")
    list_parser.set_defaults(func=cmd_list_contract_types)

    validate_parser = sub.add_parser("validate", help="Validate a contract JSON/YAML document")
    validate_parser.add_argument("contract_type", choices=sorted(VALIDATORS.keys()))
    validate_parser.add_argument("path")
    validate_parser.set_defaults(func=cmd_validate)

    validate_contract_parser = sub.add_parser("validate-contract", help="Validate a contract JSON/YAML document")
    validate_contract_parser.add_argument("contract_type", choices=sorted(VALIDATORS.keys()))
    validate_contract_parser.add_argument("path")
    validate_contract_parser.set_defaults(func=cmd_validate)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
