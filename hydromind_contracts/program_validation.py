"""Minimal contract loaders and validators for HydroMind."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import yaml

from .models import (
    AGENT_NETWORK_REQUIRED_FIELDS,
    AGENT_NODE_PROFILE_REQUIRED_FIELDS,
    AGENT_PROFILE_REQUIRED_FIELDS,
    AGENT_SKILL_BINDING_REQUIRED_FIELDS,
    CAPABILITY_MCP_SERVER_REQUIRED_FIELDS,
    BOUNDARY_CONDITION_SET_REQUIRED_FIELDS,
    CASE_MANIFEST_REQUIRED_FIELDS,
    DISTRIBUTED_TASK_RECEIPT_REQUIRED_FIELDS,
    DISPATCH_TOPOLOGY_REQUIRED_FIELDS,
    EXECUTION_LANE_REQUIRED_FIELDS,
    EXECUTION_PROVIDER_REQUIRED_FIELDS,
    FALLBACK_POLICY_REQUIRED_FIELDS,
    FINAL_REPORT_REQUIRED_FIELDS,
    HOST_SESSION_BINDING_REQUIRED_FIELDS,
    HOURLY_SCHEDULE_RESULT_REQUIRED_FIELDS,
    LIFECYCLE_PHASE_REQUIRED_FIELDS,
    MANAGEMENT_LEVEL_REQUIRED_FIELDS,
    MCP_INVOCATION_POLICY_REQUIRED_FIELDS,
    ALGORITHM_BENCHMARK_RECORD_REQUIRED_FIELDS,
    MODEL_CAPABILITY_MATRIX_REQUIRED_FIELDS,
    MODEL_SELECTION_TRACE_REQUIRED_FIELDS,
    MODEL_DELIVERY_REQUIRED_FIELDS,
    MODEL_EVAL_SUMMARY_REQUIRED_FIELDS,
    MODEL_REGISTRY_ENTRY_REQUIRED_FIELDS,
    MODEL_ROUTING_POLICY_REQUIRED_FIELDS,
    RUNTIME_TELEMETRY_RECORD_REQUIRED_FIELDS,
    STAGE_METRIC_SUMMARY_REQUIRED_FIELDS,
    PLATFORM_CAPABILITY_REQUIRED_FIELDS,
    READINESS_BOARD_REQUIRED_FIELDS,
    RELEASE_MANIFEST_REQUIRED_FIELDS,
    REVIEW_BUNDLE_REQUIRED_FIELDS,
    ROLE_PROFILE_REQUIRED_FIELDS,
    ROLE_REASONING_SCAFFOLD_REQUIRED_FIELDS,
    SESSION_MODE_REQUIRED_FIELDS,
    SKILL_MANIFEST_REQUIRED_FIELDS,
    SKILL_EXECUTION_POLICY_REQUIRED_FIELDS,
    GATEWAY_MCP_ROUTE_REQUIRED_FIELDS,
    TARGET_VOLUME_OBJECTIVE_REQUIRED_FIELDS,
    TEAM_RUN_STATE_REQUIRED_FIELDS,
    TIER_MESSAGE_REQUIRED_FIELDS,
    TIME_WINDOW_CONSTRAINT_REQUIRED_FIELDS,
    TOOL_INVOCATION_TRACE_REQUIRED_FIELDS,
    WORKFLOW_BUSINESS_REVIEW_REQUIRED_FIELDS,
    WORKFLOW_REPORT_SECTION_REQUIRED_FIELDS,
    WORKFLOW_RUN_ALLOWED_ARTIFACT_KINDS,
    WORKFLOW_RUN_ALLOWED_WRITEBACK_KINDS,
    WORKFLOW_RUN_ALLOWED_SOURCES,
    WORKFLOW_RUN_ALLOWED_STATUSES,
    WORKFLOW_RUN_OUTPUT_REQUIRED_FIELDS,
    WORKFLOW_RUN_REQUIRED_FIELDS,
)


TEAM_RUN_STATE_ALLOWED_STATUSES = (
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
)


def _require_non_empty_string(value: Any, field_name: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string")


def _require_string_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list) or any(not isinstance(item, str) or not item.strip() for item in value):
        raise ValueError(f"{field_name} must be a list of non-empty strings")


def _require_matching_workflow_companion(
    workflow_keys: Any,
    canonical_workflow_keys: Any,
    legacy_field_name: str,
    canonical_field_name: str,
) -> None:
    _require_string_list(workflow_keys, legacy_field_name)
    _require_string_list(canonical_workflow_keys, canonical_field_name)
    if len(workflow_keys) != len(canonical_workflow_keys):
        raise ValueError(f"{canonical_field_name} must align 1:1 with {legacy_field_name}")


def _require_artifact_record_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{field_name}[{index}] must be an object")
        artifact_id = item.get("artifact_id")
        _require_non_empty_string(artifact_id, f"{field_name}[{index}].artifact_id")
        if artifact_id in seen_ids:
            raise ValueError(f"{field_name}[{index}].artifact_id must be unique")
        seen_ids.add(artifact_id)
        kind = item.get("kind")
        _require_non_empty_string(kind, f"{field_name}[{index}].kind")
        if kind not in WORKFLOW_RUN_ALLOWED_ARTIFACT_KINDS:
            allowed_kinds = ", ".join(WORKFLOW_RUN_ALLOWED_ARTIFACT_KINDS)
            raise ValueError(f"{field_name}[{index}].kind must be one of: {allowed_kinds}")
        _require_non_empty_string(item.get("pointer"), f"{field_name}[{index}].pointer")


def _require_writeback_record_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{field_name}[{index}] must be an object")
        writeback_id = item.get("writeback_id")
        _require_non_empty_string(writeback_id, f"{field_name}[{index}].writeback_id")
        if writeback_id in seen_ids:
            raise ValueError(f"{field_name}[{index}].writeback_id must be unique")
        seen_ids.add(writeback_id)
        _require_non_empty_string(item.get("intervention_id"), f"{field_name}[{index}].intervention_id")
        _require_non_empty_string(item.get("surface_id"), f"{field_name}[{index}].surface_id")
        _require_non_empty_string(item.get("action"), f"{field_name}[{index}].action")
        _require_non_empty_string(item.get("kind"), f"{field_name}[{index}].kind")
        if item.get("kind") not in WORKFLOW_RUN_ALLOWED_WRITEBACK_KINDS:
            allowed_kinds = ", ".join(WORKFLOW_RUN_ALLOWED_WRITEBACK_KINDS)
            raise ValueError(f"{field_name}[{index}].kind must be one of: {allowed_kinds}")
        _require_non_empty_string(item.get("pointer"), f"{field_name}[{index}].pointer")
        _require_non_empty_string(item.get("actor"), f"{field_name}[{index}].actor")
        _require_non_empty_string(item.get("actor_scope"), f"{field_name}[{index}].actor_scope")
        _require_non_empty_string(item.get("recorded_at"), f"{field_name}[{index}].recorded_at")


def _require_agent_network_node_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{field_name}[{index}] must be an object")
        node_id = item.get("node_id")
        _require_non_empty_string(node_id, f"{field_name}[{index}].node_id")
        if node_id in seen_ids:
            raise ValueError(f"{field_name}[{index}].node_id must be unique")
        seen_ids.add(node_id)
        _require_non_empty_string(item.get("session_id"), f"{field_name}[{index}].session_id")
        _require_non_empty_string(item.get("management_level_id"), f"{field_name}[{index}].management_level_id")
        _require_non_empty_string(item.get("required_actor_scope"), f"{field_name}[{index}].required_actor_scope")


def _require_agent_network_edge_list(value: Any, field_name: str) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    seen_ids: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"{field_name}[{index}] must be an object")
        edge_id = item.get("edge_id")
        _require_non_empty_string(edge_id, f"{field_name}[{index}].edge_id")
        if edge_id in seen_ids:
            raise ValueError(f"{field_name}[{index}].edge_id must be unique")
        seen_ids.add(edge_id)
        _require_non_empty_string(item.get("from_node_id"), f"{field_name}[{index}].from_node_id")
        _require_non_empty_string(item.get("to_node_id"), f"{field_name}[{index}].to_node_id")
        _require_non_empty_string(item.get("edge_type"), f"{field_name}[{index}].edge_type")


def load_json_document(path: str | Path) -> dict[str, Any]:
    candidate = Path(path).expanduser().resolve()
    if candidate.suffix.lower() in {".yaml", ".yml"}:
        payload = yaml.safe_load(candidate.read_text(encoding="utf-8"))
    else:
        payload = json.loads(candidate.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise TypeError(f"Expected mapping JSON in {candidate}")
    return payload


def _validate_required_fields(payload: dict[str, Any], required_fields: tuple[str, ...], contract_name: str) -> dict[str, Any]:
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise ValueError(f"{contract_name} missing required fields: {', '.join(missing)}")
    return payload


def validate_case_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, CASE_MANIFEST_REQUIRED_FIELDS, "CaseManifest")
    if validated.get("contract_type") != "CaseManifest":
        raise ValueError("CaseManifest contract_type must equal 'CaseManifest'")
    return validated


def validate_workflow_run(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, WORKFLOW_RUN_REQUIRED_FIELDS, "WorkflowRun")
    if validated.get("contract_type") != "WorkflowRun":
        raise ValueError("WorkflowRun contract_type must equal 'WorkflowRun'")
    _require_non_empty_string(validated.get("case_id"), "WorkflowRun case_id")
    _require_non_empty_string(validated.get("workflow_name"), "WorkflowRun workflow_name")
    _require_non_empty_string(validated.get("canonical_workflow_key"), "WorkflowRun canonical_workflow_key")
    _require_non_empty_string(validated.get("run_id"), "WorkflowRun run_id")
    _require_non_empty_string(validated.get("started_at"), "WorkflowRun started_at")
    _require_non_empty_string(validated.get("finished_at"), "WorkflowRun finished_at")

    status = validated.get("status")
    if status not in WORKFLOW_RUN_ALLOWED_STATUSES:
        allowed_statuses = ", ".join(WORKFLOW_RUN_ALLOWED_STATUSES)
        raise ValueError(f"WorkflowRun status must be one of: {allowed_statuses}")

    inputs = validated.get("inputs")
    if not isinstance(inputs, dict):
        raise ValueError("WorkflowRun inputs must be an object")
    _require_non_empty_string(inputs.get("session_id"), "WorkflowRun inputs.session_id")
    _require_non_empty_string(inputs.get("profile"), "WorkflowRun inputs.profile")

    outputs = validated.get("outputs")
    if not isinstance(outputs, dict):
        raise ValueError("WorkflowRun outputs must be an object")
    _validate_required_fields(outputs, WORKFLOW_RUN_OUTPUT_REQUIRED_FIELDS, "WorkflowRun outputs")

    source = outputs.get("source")
    if source not in WORKFLOW_RUN_ALLOWED_SOURCES:
        allowed_sources = ", ".join(WORKFLOW_RUN_ALLOWED_SOURCES)
        raise ValueError(f"WorkflowRun outputs.source must be one of: {allowed_sources}")
    if outputs.get("terminal_status") != status:
        raise ValueError("WorkflowRun outputs.terminal_status must equal WorkflowRun status")
    _require_non_empty_string(outputs.get("provider_id"), "WorkflowRun outputs.provider_id")
    _require_non_empty_string(outputs.get("adapter_type"), "WorkflowRun outputs.adapter_type")

    artifacts = outputs.get("artifacts")
    if not isinstance(artifacts, (dict, list)):
        raise ValueError("WorkflowRun outputs.artifacts must be an object or list")
    artifact_records = outputs.get("artifact_records")
    _require_artifact_record_list(artifact_records, "WorkflowRun outputs.artifact_records")
    writeback_records = outputs.get("writeback_records")
    if writeback_records is not None:
        _require_writeback_record_list(writeback_records, "WorkflowRun outputs.writeback_records")

    if "trace_id" in validated:
        _require_non_empty_string(validated.get("trace_id"), "WorkflowRun trace_id")
    if "trace_pointer" in validated:
        _require_non_empty_string(validated.get("trace_pointer"), "WorkflowRun trace_pointer")
    if "trace_id" not in validated and "trace_pointer" not in validated:
        raise ValueError("WorkflowRun must include trace_id or trace_pointer")
    if "trace_id" in outputs:
        _require_non_empty_string(outputs.get("trace_id"), "WorkflowRun outputs.trace_id")
    if "trace_id" in validated:
        if outputs.get("trace_id") != validated.get("trace_id"):
            raise ValueError("WorkflowRun outputs.trace_id must equal WorkflowRun trace_id")

    if not isinstance(validated.get("trace_summary"), dict):
        raise ValueError("WorkflowRun trace_summary must be an object")
    _require_string_list(validated.get("contracts_emitted"), "WorkflowRun contracts_emitted")
    _require_string_list(validated.get("artifacts_emitted"), "WorkflowRun artifacts_emitted")
    artifact_ids = [record["artifact_id"] for record in artifact_records]
    if validated.get("artifacts_emitted") != artifact_ids:
        raise ValueError("WorkflowRun artifacts_emitted must equal WorkflowRun outputs.artifact_records artifact_id order")
    return validated


def validate_final_report(payload: dict[str, Any]) -> dict[str, Any]:
    return _validate_required_fields(payload, FINAL_REPORT_REQUIRED_FIELDS, "FinalReport")


def validate_dispatch_topology(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, DISPATCH_TOPOLOGY_REQUIRED_FIELDS, "DispatchTopology")
    if validated.get("contract_type") != "DispatchTopology":
        raise ValueError("DispatchTopology contract_type must equal 'DispatchTopology'")
    _require_non_empty_string(validated.get("case_id"), "DispatchTopology case_id")
    _require_non_empty_string(validated.get("topology_id"), "DispatchTopology topology_id")
    _require_non_empty_string(validated.get("network_type"), "DispatchTopology network_type")
    if not isinstance(validated.get("corridors"), list):
        raise ValueError("DispatchTopology corridors must be a list")
    if not isinstance(validated.get("nodes"), list):
        raise ValueError("DispatchTopology nodes must be a list")
    if not isinstance(validated.get("edges"), list):
        raise ValueError("DispatchTopology edges must be a list")
    return validated


def validate_target_volume_objective(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, TARGET_VOLUME_OBJECTIVE_REQUIRED_FIELDS, "TargetVolumeObjective")
    if validated.get("contract_type") != "TargetVolumeObjective":
        raise ValueError("TargetVolumeObjective contract_type must equal 'TargetVolumeObjective'")
    _require_non_empty_string(validated.get("case_id"), "TargetVolumeObjective case_id")
    _require_non_empty_string(validated.get("objective_id"), "TargetVolumeObjective objective_id")
    _require_non_empty_string(validated.get("objective_type"), "TargetVolumeObjective objective_type")
    if not isinstance(validated.get("target_volume_m3"), (int, float)):
        raise ValueError("TargetVolumeObjective target_volume_m3 must be numeric")
    if not isinstance(validated.get("horizon_hours"), int) or validated["horizon_hours"] <= 0:
        raise ValueError("TargetVolumeObjective horizon_hours must be a positive integer")
    return validated


def validate_time_window_constraint(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, TIME_WINDOW_CONSTRAINT_REQUIRED_FIELDS, "TimeWindowConstraint")
    if validated.get("contract_type") != "TimeWindowConstraint":
        raise ValueError("TimeWindowConstraint contract_type must equal 'TimeWindowConstraint'")
    _require_non_empty_string(validated.get("case_id"), "TimeWindowConstraint case_id")
    _require_non_empty_string(validated.get("constraint_id"), "TimeWindowConstraint constraint_id")
    if not isinstance(validated.get("horizon_hours"), int) or validated["horizon_hours"] <= 0:
        raise ValueError("TimeWindowConstraint horizon_hours must be a positive integer")
    periods = validated.get("allowed_periods")
    if not isinstance(periods, list) or any(item not in (0, 1) for item in periods):
        raise ValueError("TimeWindowConstraint allowed_periods must be a list of 0/1 integers")
    return validated


def validate_boundary_condition_set(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, BOUNDARY_CONDITION_SET_REQUIRED_FIELDS, "BoundaryConditionSet")
    if validated.get("contract_type") != "BoundaryConditionSet":
        raise ValueError("BoundaryConditionSet contract_type must equal 'BoundaryConditionSet'")
    _require_non_empty_string(validated.get("case_id"), "BoundaryConditionSet case_id")
    _require_non_empty_string(validated.get("condition_set_id"), "BoundaryConditionSet condition_set_id")
    if not isinstance(validated.get("horizon_hours"), int) or validated["horizon_hours"] <= 0:
        raise ValueError("BoundaryConditionSet horizon_hours must be a positive integer")
    if not isinstance(validated.get("boundary_conditions"), list):
        raise ValueError("BoundaryConditionSet boundary_conditions must be a list")
    return validated


def validate_hourly_schedule_result(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, HOURLY_SCHEDULE_RESULT_REQUIRED_FIELDS, "HourlyScheduleResult")
    if validated.get("contract_type") != "HourlyScheduleResult":
        raise ValueError("HourlyScheduleResult contract_type must equal 'HourlyScheduleResult'")
    _require_non_empty_string(validated.get("case_id"), "HourlyScheduleResult case_id")
    _require_non_empty_string(validated.get("schedule_id"), "HourlyScheduleResult schedule_id")
    _require_non_empty_string(validated.get("status"), "HourlyScheduleResult status")
    if not isinstance(validated.get("horizon_hours"), int) or validated["horizon_hours"] <= 0:
        raise ValueError("HourlyScheduleResult horizon_hours must be a positive integer")
    _require_non_empty_string(validated.get("objective_ref"), "HourlyScheduleResult objective_ref")
    _require_non_empty_string(validated.get("time_window_ref"), "HourlyScheduleResult time_window_ref")
    _require_non_empty_string(validated.get("boundary_condition_ref"), "HourlyScheduleResult boundary_condition_ref")
    if not isinstance(validated.get("timeline"), list):
        raise ValueError("HourlyScheduleResult timeline must be a list")
    return validated


def validate_readiness_board(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, READINESS_BOARD_REQUIRED_FIELDS, "ReadinessBoard")
    if validated.get("contract_type") != "ReadinessBoard":
        raise ValueError("ReadinessBoard contract_type must equal 'ReadinessBoard'")
    return validated


def validate_review_bundle(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, REVIEW_BUNDLE_REQUIRED_FIELDS, "ReviewBundle")
    if validated.get("contract_type") != "ReviewBundle":
        raise ValueError("ReviewBundle contract_type must equal 'ReviewBundle'")
    return validated


def validate_release_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, RELEASE_MANIFEST_REQUIRED_FIELDS, "ReleaseManifest")
    if validated.get("contract_type") != "ReleaseManifest":
        raise ValueError("ReleaseManifest contract_type must equal 'ReleaseManifest'")
    return validated


def validate_platform_capability(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, PLATFORM_CAPABILITY_REQUIRED_FIELDS, "PlatformCapability")
    if validated.get("contract_type") != "PlatformCapability":
        raise ValueError("PlatformCapability contract_type must equal 'PlatformCapability'")
    return validated


def validate_execution_provider(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, EXECUTION_PROVIDER_REQUIRED_FIELDS, "ExecutionProvider")
    if validated.get("contract_type") != "ExecutionProvider":
        raise ValueError("ExecutionProvider contract_type must equal 'ExecutionProvider'")
    return validated


def validate_host_session_binding(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, HOST_SESSION_BINDING_REQUIRED_FIELDS, "HostSessionBinding")
    if validated.get("contract_type") != "HostSessionBinding":
        raise ValueError("HostSessionBinding contract_type must equal 'HostSessionBinding'")
    return validated


def validate_team_run_state(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, TEAM_RUN_STATE_REQUIRED_FIELDS, "TeamRunState")
    if validated.get("contract_type") != "TeamRunState":
        raise ValueError("TeamRunState contract_type must equal 'TeamRunState'")
    if validated.get("status") not in TEAM_RUN_STATE_ALLOWED_STATUSES:
        allowed_statuses = ", ".join(TEAM_RUN_STATE_ALLOWED_STATUSES)
        raise ValueError(f"TeamRunState status must be one of: {allowed_statuses}")
    _require_non_empty_string(validated.get("session_id"), "TeamRunState session_id")

    workflow_runs = validated.get("workflow_runs")
    if workflow_runs is not None:
        if not isinstance(workflow_runs, list):
            raise ValueError("TeamRunState workflow_runs must be a list")
        seen_run_ids: set[str] = set()
        case_id = validated.get("case_id")
        session_id_prefix = f"{validated['session_id']}:"
        for workflow_run in workflow_runs:
            if not isinstance(workflow_run, dict):
                raise ValueError("TeamRunState workflow_runs entries must be objects")
            validated_workflow_run = validate_workflow_run(workflow_run)
            run_id = validated_workflow_run["run_id"]
            if run_id in seen_run_ids:
                raise ValueError(f"TeamRunState workflow_runs contains duplicate run_id: {run_id}")
            seen_run_ids.add(run_id)
            if case_id is not None and validated_workflow_run.get("case_id") != case_id:
                raise ValueError("TeamRunState workflow_runs case_id must match TeamRunState case_id")
            if not run_id.startswith(session_id_prefix):
                raise ValueError("TeamRunState workflow_runs run_id must start with TeamRunState session_id")
    tool_invocation_traces = validated.get("tool_invocation_traces")
    if tool_invocation_traces is not None:
        if not isinstance(tool_invocation_traces, list):
            raise ValueError("TeamRunState tool_invocation_traces must be a list")
        seen_trace_ids: set[str] = set()
        case_id = validated.get("case_id")
        session_id = str(validated.get("session_id") or "").strip()
        for trace in tool_invocation_traces:
            if not isinstance(trace, dict):
                raise ValueError("TeamRunState tool_invocation_traces entries must be objects")
            validated_trace = validate_tool_invocation_trace(trace)
            trace_id = validated_trace["trace_id"]
            if trace_id in seen_trace_ids:
                raise ValueError(f"TeamRunState tool_invocation_traces contains duplicate trace_id: {trace_id}")
            seen_trace_ids.add(trace_id)
            if case_id is not None and validated_trace.get("case_id") != case_id:
                raise ValueError("TeamRunState tool_invocation_traces case_id must match TeamRunState case_id")
            if str(validated_trace.get("session_id") or "").strip() != session_id:
                raise ValueError("TeamRunState tool_invocation_traces session_id must match TeamRunState session_id")
    distributed_task_receipts = validated.get("distributed_task_receipts")
    if distributed_task_receipts is not None:
        if not isinstance(distributed_task_receipts, list):
            raise ValueError("TeamRunState distributed_task_receipts must be a list")
        seen_receipt_ids: set[str] = set()
        case_id = validated.get("case_id")
        session_id = str(validated.get("session_id") or "").strip()
        for receipt in distributed_task_receipts:
            if not isinstance(receipt, dict):
                raise ValueError("TeamRunState distributed_task_receipts entries must be objects")
            validated_receipt = validate_distributed_task_receipt(receipt)
            receipt_id = validated_receipt["receipt_id"]
            if receipt_id in seen_receipt_ids:
                raise ValueError(f"TeamRunState distributed_task_receipts contains duplicate receipt_id: {receipt_id}")
            seen_receipt_ids.add(receipt_id)
            if case_id is not None and validated_receipt.get("case_id") != case_id:
                raise ValueError("TeamRunState distributed_task_receipts case_id must match TeamRunState case_id")
            if str(validated_receipt.get("session_id") or "").strip() != session_id:
                raise ValueError("TeamRunState distributed_task_receipts session_id must match TeamRunState session_id")
    model_selection_traces = validated.get("model_selection_traces")
    if model_selection_traces is not None:
        if not isinstance(model_selection_traces, list):
            raise ValueError("TeamRunState model_selection_traces must be a list")
        seen_selection_trace_ids: set[str] = set()
        case_id = validated.get("case_id")
        session_id = str(validated.get("session_id") or "").strip()
        for trace in model_selection_traces:
            if not isinstance(trace, dict):
                raise ValueError("TeamRunState model_selection_traces entries must be objects")
            validated_trace = validate_model_selection_trace(trace)
            trace_id = validated_trace["selection_trace_id"]
            if trace_id in seen_selection_trace_ids:
                raise ValueError(f"TeamRunState model_selection_traces contains duplicate selection_trace_id: {trace_id}")
            seen_selection_trace_ids.add(trace_id)
            if case_id is not None and validated_trace.get("case_id") != case_id:
                raise ValueError("TeamRunState model_selection_traces case_id must match TeamRunState case_id")
            if str(validated_trace.get("session_id") or "").strip() != session_id:
                raise ValueError("TeamRunState model_selection_traces session_id must match TeamRunState session_id")
    runtime_telemetry_records = validated.get("runtime_telemetry_records")
    if runtime_telemetry_records is not None:
        if not isinstance(runtime_telemetry_records, list):
            raise ValueError("TeamRunState runtime_telemetry_records must be a list")
        seen_telemetry_ids: set[str] = set()
        case_id = validated.get("case_id")
        session_id = str(validated.get("session_id") or "").strip()
        for record in runtime_telemetry_records:
            if not isinstance(record, dict):
                raise ValueError("TeamRunState runtime_telemetry_records entries must be objects")
            validated_record = validate_runtime_telemetry_record(record)
            telemetry_id = validated_record["telemetry_id"]
            if telemetry_id in seen_telemetry_ids:
                raise ValueError(f"TeamRunState runtime_telemetry_records contains duplicate telemetry_id: {telemetry_id}")
            seen_telemetry_ids.add(telemetry_id)
            if case_id is not None and validated_record.get("case_id") != case_id:
                raise ValueError("TeamRunState runtime_telemetry_records case_id must match TeamRunState case_id")
            if str(validated_record.get("session_id") or "").strip() != session_id:
                raise ValueError("TeamRunState runtime_telemetry_records session_id must match TeamRunState session_id")
    return validated


def validate_lifecycle_phase(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, LIFECYCLE_PHASE_REQUIRED_FIELDS, "LifecyclePhase")
    if validated.get("contract_type") != "LifecyclePhase":
        raise ValueError("LifecyclePhase contract_type must equal 'LifecyclePhase'")
    _require_non_empty_string(validated.get("lifecycle_stage_id"), "LifecyclePhase lifecycle_stage_id")
    _require_non_empty_string(validated.get("display_name"), "LifecyclePhase display_name")
    _require_non_empty_string(validated.get("mission"), "LifecyclePhase mission")
    _require_string_list(validated.get("outputs"), "LifecyclePhase outputs")
    return validated


def validate_management_level(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MANAGEMENT_LEVEL_REQUIRED_FIELDS, "ManagementLevel")
    if validated.get("contract_type") != "ManagementLevel":
        raise ValueError("ManagementLevel contract_type must equal 'ManagementLevel'")
    _require_non_empty_string(validated.get("management_level_id"), "ManagementLevel management_level_id")
    _require_non_empty_string(validated.get("display_name"), "ManagementLevel display_name")
    _require_non_empty_string(validated.get("scope"), "ManagementLevel scope")
    _require_string_list(validated.get("responsibilities"), "ManagementLevel responsibilities")
    return validated


def validate_role_profile(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, ROLE_PROFILE_REQUIRED_FIELDS, "RoleProfile")
    if validated.get("contract_type") != "RoleProfile":
        raise ValueError("RoleProfile contract_type must equal 'RoleProfile'")
    _require_non_empty_string(validated.get("role_profile_id"), "RoleProfile role_profile_id")
    _require_non_empty_string(validated.get("display_name"), "RoleProfile display_name")
    _require_non_empty_string(validated.get("lifecycle_stage_id"), "RoleProfile lifecycle_stage_id")
    _require_non_empty_string(validated.get("default_management_level_id"), "RoleProfile default_management_level_id")
    _require_string_list(validated.get("workflow_focus"), "RoleProfile workflow_focus")
    return validated


def validate_agent_node_profile(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, AGENT_NODE_PROFILE_REQUIRED_FIELDS, "AgentNodeProfile")
    if validated.get("contract_type") != "AgentNodeProfile":
        raise ValueError("AgentNodeProfile contract_type must equal 'AgentNodeProfile'")
    _require_non_empty_string(validated.get("agent_node_profile_id"), "AgentNodeProfile agent_node_profile_id")
    _require_non_empty_string(validated.get("display_name"), "AgentNodeProfile display_name")
    _require_non_empty_string(validated.get("lifecycle_stage_id"), "AgentNodeProfile lifecycle_stage_id")
    _require_non_empty_string(validated.get("management_level_id"), "AgentNodeProfile management_level_id")
    _require_non_empty_string(validated.get("role_profile_id"), "AgentNodeProfile role_profile_id")
    _require_non_empty_string(validated.get("scope_pattern"), "AgentNodeProfile scope_pattern")
    return validated


def validate_session_mode(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, SESSION_MODE_REQUIRED_FIELDS, "SessionMode")
    if validated.get("contract_type") != "SessionMode":
        raise ValueError("SessionMode contract_type must equal 'SessionMode'")
    _require_non_empty_string(validated.get("agent_session_mode_id"), "SessionMode agent_session_mode_id")
    _require_non_empty_string(validated.get("display_name"), "SessionMode display_name")
    _require_non_empty_string(validated.get("human_interaction"), "SessionMode human_interaction")
    return validated


def validate_agent_profile(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, AGENT_PROFILE_REQUIRED_FIELDS, "AgentProfile")
    if validated.get("contract_type") != "AgentProfile":
        raise ValueError("AgentProfile contract_type must equal 'AgentProfile'")
    _require_non_empty_string(validated.get("agent_profile_id"), "AgentProfile agent_profile_id")
    _require_non_empty_string(validated.get("display_name"), "AgentProfile display_name")
    _require_non_empty_string(validated.get("role_id"), "AgentProfile role_id")
    _require_non_empty_string(validated.get("role_profile_id"), "AgentProfile role_profile_id")
    _require_non_empty_string(validated.get("lifecycle_stage_id"), "AgentProfile lifecycle_stage_id")
    _require_non_empty_string(validated.get("management_level_id"), "AgentProfile management_level_id")
    _require_non_empty_string(validated.get("default_session_mode_id"), "AgentProfile default_session_mode_id")
    _require_string_list(validated.get("supported_skill_ids"), "AgentProfile supported_skill_ids")
    return validated


def validate_skill_manifest(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, SKILL_MANIFEST_REQUIRED_FIELDS, "SkillManifest")
    if validated.get("contract_type") != "SkillManifest":
        raise ValueError("SkillManifest contract_type must equal 'SkillManifest'")
    _require_non_empty_string(validated.get("skill_id"), "SkillManifest skill_id")
    _require_non_empty_string(validated.get("display_name"), "SkillManifest display_name")
    _require_non_empty_string(validated.get("category"), "SkillManifest category")
    _require_string_list(validated.get("lifecycle_stage_ids"), "SkillManifest lifecycle_stage_ids")
    _require_matching_workflow_companion(
        validated.get("workflow_keys"),
        validated.get("canonical_workflow_keys"),
        "SkillManifest workflow_keys",
        "SkillManifest canonical_workflow_keys",
    )
    _require_non_empty_string(validated.get("entry_command"), "SkillManifest entry_command")
    return validated


def validate_agent_skill_binding(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, AGENT_SKILL_BINDING_REQUIRED_FIELDS, "AgentSkillBinding")
    if validated.get("contract_type") != "AgentSkillBinding":
        raise ValueError("AgentSkillBinding contract_type must equal 'AgentSkillBinding'")
    _require_non_empty_string(validated.get("binding_id"), "AgentSkillBinding binding_id")
    _require_non_empty_string(validated.get("agent_profile_id"), "AgentSkillBinding agent_profile_id")
    _require_non_empty_string(validated.get("skill_id"), "AgentSkillBinding skill_id")
    _require_non_empty_string(validated.get("activation_mode"), "AgentSkillBinding activation_mode")
    return validated


def validate_role_reasoning_scaffold(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, ROLE_REASONING_SCAFFOLD_REQUIRED_FIELDS, "RoleReasoningScaffold")
    if validated.get("contract_type") != "RoleReasoningScaffold":
        raise ValueError("RoleReasoningScaffold contract_type must equal 'RoleReasoningScaffold'")
    _require_non_empty_string(validated.get("scaffold_id"), "RoleReasoningScaffold scaffold_id")
    _require_non_empty_string(validated.get("role_id"), "RoleReasoningScaffold role_id")
    _require_string_list(validated.get("lifecycle_stage_ids"), "RoleReasoningScaffold lifecycle_stage_ids")
    _require_string_list(validated.get("goal_types"), "RoleReasoningScaffold goal_types")
    _require_string_list(validated.get("required_context_slots"), "RoleReasoningScaffold required_context_slots")
    _require_string_list(validated.get("decision_steps"), "RoleReasoningScaffold decision_steps")
    _require_string_list(validated.get("required_evidence"), "RoleReasoningScaffold required_evidence")
    _require_string_list(validated.get("forbidden_shortcuts"), "RoleReasoningScaffold forbidden_shortcuts")
    _require_string_list(validated.get("handoff_rules"), "RoleReasoningScaffold handoff_rules")
    return validated


def validate_skill_execution_policy(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, SKILL_EXECUTION_POLICY_REQUIRED_FIELDS, "SkillExecutionPolicy")
    if validated.get("contract_type") != "SkillExecutionPolicy":
        raise ValueError("SkillExecutionPolicy contract_type must equal 'SkillExecutionPolicy'")
    _require_non_empty_string(validated.get("policy_id"), "SkillExecutionPolicy policy_id")
    _require_non_empty_string(validated.get("skill_id"), "SkillExecutionPolicy skill_id")
    _require_string_list(validated.get("entry_conditions"), "SkillExecutionPolicy entry_conditions")
    _require_string_list(validated.get("required_inputs"), "SkillExecutionPolicy required_inputs")
    _require_string_list(validated.get("execution_steps"), "SkillExecutionPolicy execution_steps")
    _require_string_list(validated.get("preferred_mcp_sequence"), "SkillExecutionPolicy preferred_mcp_sequence")
    _require_string_list(validated.get("fallback_steps"), "SkillExecutionPolicy fallback_steps")
    _require_string_list(validated.get("quality_gates"), "SkillExecutionPolicy quality_gates")
    _require_string_list(validated.get("result_schema_expectation"), "SkillExecutionPolicy result_schema_expectation")
    return validated


def validate_mcp_invocation_policy(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MCP_INVOCATION_POLICY_REQUIRED_FIELDS, "McpInvocationPolicy")
    if validated.get("contract_type") != "McpInvocationPolicy":
        raise ValueError("McpInvocationPolicy contract_type must equal 'McpInvocationPolicy'")
    _require_non_empty_string(validated.get("policy_id"), "McpInvocationPolicy policy_id")
    _require_non_empty_string(validated.get("mcp_group"), "McpInvocationPolicy mcp_group")
    _require_string_list(validated.get("capability_server_ids"), "McpInvocationPolicy capability_server_ids")
    _require_string_list(validated.get("gateway_route_ids"), "McpInvocationPolicy gateway_route_ids")
    _require_string_list(validated.get("supported_tasks"), "McpInvocationPolicy supported_tasks")
    parameter_templates = validated.get("parameter_templates")
    if not isinstance(parameter_templates, dict) or not parameter_templates:
        raise ValueError("McpInvocationPolicy parameter_templates must be a non-empty object")
    _require_string_list(validated.get("invocation_sequence"), "McpInvocationPolicy invocation_sequence")
    _require_non_empty_string(validated.get("retry_policy"), "McpInvocationPolicy retry_policy")
    _require_non_empty_string(validated.get("fallback_policy"), "McpInvocationPolicy fallback_policy")
    _require_string_list(validated.get("trace_requirements"), "McpInvocationPolicy trace_requirements")
    return validated


def validate_capability_mcp_server(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, CAPABILITY_MCP_SERVER_REQUIRED_FIELDS, "CapabilityMcpServer")
    if validated.get("contract_type") != "CapabilityMcpServer":
        raise ValueError("CapabilityMcpServer contract_type must equal 'CapabilityMcpServer'")
    _require_non_empty_string(validated.get("server_id"), "CapabilityMcpServer server_id")
    _require_non_empty_string(validated.get("display_name"), "CapabilityMcpServer display_name")
    _require_non_empty_string(validated.get("server_kind"), "CapabilityMcpServer server_kind")
    _require_non_empty_string(validated.get("transport"), "CapabilityMcpServer transport")
    _require_string_list(validated.get("tool_ids"), "CapabilityMcpServer tool_ids")
    _require_string_list(validated.get("supported_task_types"), "CapabilityMcpServer supported_task_types")
    return validated


def validate_gateway_mcp_route(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, GATEWAY_MCP_ROUTE_REQUIRED_FIELDS, "GatewayMcpRoute")
    if validated.get("contract_type") != "GatewayMcpRoute":
        raise ValueError("GatewayMcpRoute contract_type must equal 'GatewayMcpRoute'")
    _require_non_empty_string(validated.get("route_id"), "GatewayMcpRoute route_id")
    _require_non_empty_string(validated.get("display_name"), "GatewayMcpRoute display_name")
    _require_non_empty_string(validated.get("gateway_kind"), "GatewayMcpRoute gateway_kind")
    _require_non_empty_string(validated.get("entrypoint"), "GatewayMcpRoute entrypoint")
    _require_string_list(validated.get("capability_server_ids"), "GatewayMcpRoute capability_server_ids")
    _require_matching_workflow_companion(
        validated.get("supported_workflows"),
        validated.get("supported_canonical_workflow_keys"),
        "GatewayMcpRoute supported_workflows",
        "GatewayMcpRoute supported_canonical_workflow_keys",
    )
    _require_non_empty_string(validated.get("invocation_mode"), "GatewayMcpRoute invocation_mode")
    return validated


def validate_tool_invocation_trace(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, TOOL_INVOCATION_TRACE_REQUIRED_FIELDS, "ToolInvocationTrace")
    if validated.get("contract_type") != "ToolInvocationTrace":
        raise ValueError("ToolInvocationTrace contract_type must equal 'ToolInvocationTrace'")
    _require_non_empty_string(validated.get("trace_id"), "ToolInvocationTrace trace_id")
    _require_non_empty_string(validated.get("case_id"), "ToolInvocationTrace case_id")
    _require_non_empty_string(validated.get("route_id"), "ToolInvocationTrace route_id")
    _require_non_empty_string(validated.get("server_id"), "ToolInvocationTrace server_id")
    _require_non_empty_string(validated.get("tool_name"), "ToolInvocationTrace tool_name")
    _require_non_empty_string(validated.get("status"), "ToolInvocationTrace status")
    _require_non_empty_string(validated.get("recorded_at"), "ToolInvocationTrace recorded_at")
    return validated


def validate_execution_lane(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, EXECUTION_LANE_REQUIRED_FIELDS, "ExecutionLane")
    if validated.get("contract_type") != "ExecutionLane":
        raise ValueError("ExecutionLane contract_type must equal 'ExecutionLane'")
    _require_non_empty_string(validated.get("lane_id"), "ExecutionLane lane_id")
    _require_non_empty_string(validated.get("display_name"), "ExecutionLane display_name")
    _require_non_empty_string(validated.get("provider_id"), "ExecutionLane provider_id")
    _require_non_empty_string(validated.get("adapter_type"), "ExecutionLane adapter_type")
    _require_matching_workflow_companion(
        validated.get("supported_workflows"),
        validated.get("supported_canonical_workflow_keys"),
        "ExecutionLane supported_workflows",
        "ExecutionLane supported_canonical_workflow_keys",
    )
    _require_non_empty_string(validated.get("runtime_class"), "ExecutionLane runtime_class")
    _require_non_empty_string(validated.get("dispatch_mode"), "ExecutionLane dispatch_mode")
    _require_non_empty_string(validated.get("artifact_root_kind"), "ExecutionLane artifact_root_kind")
    _require_non_empty_string(validated.get("status"), "ExecutionLane status")
    return validated


def validate_fallback_policy(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, FALLBACK_POLICY_REQUIRED_FIELDS, "FallbackPolicy")
    if validated.get("contract_type") != "FallbackPolicy":
        raise ValueError("FallbackPolicy contract_type must equal 'FallbackPolicy'")
    _require_non_empty_string(validated.get("fallback_policy_id"), "FallbackPolicy fallback_policy_id")
    _require_non_empty_string(validated.get("display_name"), "FallbackPolicy display_name")
    _require_matching_workflow_companion(
        validated.get("supported_workflows"),
        validated.get("supported_canonical_workflow_keys"),
        "FallbackPolicy supported_workflows",
        "FallbackPolicy supported_canonical_workflow_keys",
    )
    _require_non_empty_string(validated.get("primary_lane_id"), "FallbackPolicy primary_lane_id")
    _require_string_list(validated.get("fallback_lane_ids"), "FallbackPolicy fallback_lane_ids")
    _require_non_empty_string(validated.get("degrade_mode"), "FallbackPolicy degrade_mode")
    retry_budget = validated.get("retry_budget")
    if not isinstance(retry_budget, int) or retry_budget < 0:
        raise ValueError("FallbackPolicy retry_budget must be a non-negative integer")
    _require_string_list(validated.get("terminal_conditions"), "FallbackPolicy terminal_conditions")
    return validated


def validate_distributed_task_receipt(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, DISTRIBUTED_TASK_RECEIPT_REQUIRED_FIELDS, "DistributedTaskReceipt")
    if validated.get("contract_type") != "DistributedTaskReceipt":
        raise ValueError("DistributedTaskReceipt contract_type must equal 'DistributedTaskReceipt'")
    _require_non_empty_string(validated.get("receipt_id"), "DistributedTaskReceipt receipt_id")
    _require_non_empty_string(validated.get("session_id"), "DistributedTaskReceipt session_id")
    _require_non_empty_string(validated.get("case_id"), "DistributedTaskReceipt case_id")
    _require_non_empty_string(validated.get("workflow_name"), "DistributedTaskReceipt workflow_name")
    _require_non_empty_string(validated.get("canonical_workflow_key"), "DistributedTaskReceipt canonical_workflow_key")
    _require_non_empty_string(validated.get("lane_id"), "DistributedTaskReceipt lane_id")
    _require_non_empty_string(validated.get("fallback_policy_id"), "DistributedTaskReceipt fallback_policy_id")
    _require_non_empty_string(validated.get("provider_id"), "DistributedTaskReceipt provider_id")
    _require_non_empty_string(validated.get("adapter_type"), "DistributedTaskReceipt adapter_type")
    _require_non_empty_string(validated.get("status"), "DistributedTaskReceipt status")
    _require_non_empty_string(validated.get("started_at"), "DistributedTaskReceipt started_at")
    _require_non_empty_string(validated.get("finished_at"), "DistributedTaskReceipt finished_at")
    _require_string_list(validated.get("artifact_refs"), "DistributedTaskReceipt artifact_refs")
    return validated


def validate_model_selection_trace(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MODEL_SELECTION_TRACE_REQUIRED_FIELDS, "ModelSelectionTrace")
    if validated.get("contract_type") != "ModelSelectionTrace":
        raise ValueError("ModelSelectionTrace contract_type must equal 'ModelSelectionTrace'")
    _require_non_empty_string(validated.get("selection_trace_id"), "ModelSelectionTrace selection_trace_id")
    _require_non_empty_string(validated.get("session_id"), "ModelSelectionTrace session_id")
    _require_non_empty_string(validated.get("case_id"), "ModelSelectionTrace case_id")
    _require_non_empty_string(validated.get("workflow_name"), "ModelSelectionTrace workflow_name")
    _require_non_empty_string(validated.get("canonical_workflow_key"), "ModelSelectionTrace canonical_workflow_key")
    _require_non_empty_string(validated.get("role_id"), "ModelSelectionTrace role_id")
    _require_non_empty_string(validated.get("lifecycle_stage_id"), "ModelSelectionTrace lifecycle_stage_id")
    _require_non_empty_string(validated.get("policy_id"), "ModelSelectionTrace policy_id")
    _require_non_empty_string(validated.get("preferred_model_id"), "ModelSelectionTrace preferred_model_id")
    _require_string_list(validated.get("fallback_model_ids"), "ModelSelectionTrace fallback_model_ids")
    _require_string_list(validated.get("required_model_capability_tags"), "ModelSelectionTrace required_model_capability_tags")
    _require_string_list(validated.get("eval_summary_ids"), "ModelSelectionTrace eval_summary_ids")
    _require_non_empty_string(validated.get("status"), "ModelSelectionTrace status")
    _require_non_empty_string(validated.get("recorded_at"), "ModelSelectionTrace recorded_at")
    return validated


def validate_runtime_telemetry_record(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, RUNTIME_TELEMETRY_RECORD_REQUIRED_FIELDS, "RuntimeTelemetryRecord")
    if validated.get("contract_type") != "RuntimeTelemetryRecord":
        raise ValueError("RuntimeTelemetryRecord contract_type must equal 'RuntimeTelemetryRecord'")
    _require_non_empty_string(validated.get("telemetry_id"), "RuntimeTelemetryRecord telemetry_id")
    _require_non_empty_string(validated.get("session_id"), "RuntimeTelemetryRecord session_id")
    _require_non_empty_string(validated.get("case_id"), "RuntimeTelemetryRecord case_id")
    _require_non_empty_string(validated.get("workflow_name"), "RuntimeTelemetryRecord workflow_name")
    _require_non_empty_string(validated.get("canonical_workflow_key"), "RuntimeTelemetryRecord canonical_workflow_key")
    _require_non_empty_string(validated.get("status"), "RuntimeTelemetryRecord status")
    _require_non_empty_string(validated.get("selection_trace_id"), "RuntimeTelemetryRecord selection_trace_id")
    _require_non_empty_string(validated.get("model_policy_id"), "RuntimeTelemetryRecord model_policy_id")
    _require_non_empty_string(validated.get("preferred_model_id"), "RuntimeTelemetryRecord preferred_model_id")
    _require_string_list(validated.get("route_ids"), "RuntimeTelemetryRecord route_ids")
    _require_string_list(validated.get("server_ids"), "RuntimeTelemetryRecord server_ids")
    _require_non_empty_string(validated.get("lane_id"), "RuntimeTelemetryRecord lane_id")
    _require_non_empty_string(validated.get("fallback_policy_id"), "RuntimeTelemetryRecord fallback_policy_id")
    _require_non_empty_string(validated.get("distributed_task_receipt_id"), "RuntimeTelemetryRecord distributed_task_receipt_id")
    _require_string_list(validated.get("tool_trace_ids"), "RuntimeTelemetryRecord tool_trace_ids")
    _require_string_list(validated.get("artifact_refs"), "RuntimeTelemetryRecord artifact_refs")
    _require_non_empty_string(validated.get("started_at"), "RuntimeTelemetryRecord started_at")
    _require_non_empty_string(validated.get("finished_at"), "RuntimeTelemetryRecord finished_at")
    return validated


def validate_stage_metric_summary(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, STAGE_METRIC_SUMMARY_REQUIRED_FIELDS, "StageMetricSummary")
    if validated.get("contract_type") != "StageMetricSummary":
        raise ValueError("StageMetricSummary contract_type must equal 'StageMetricSummary'")
    _require_non_empty_string(validated.get("metric_summary_id"), "StageMetricSummary metric_summary_id")
    _require_non_empty_string(validated.get("case_id"), "StageMetricSummary case_id")
    _require_non_empty_string(validated.get("stage_id"), "StageMetricSummary stage_id")
    _require_string_list(validated.get("metric_dimensions"), "StageMetricSummary metric_dimensions")
    _require_string_list(validated.get("covered_dimension_ids"), "StageMetricSummary covered_dimension_ids")
    _require_string_list(validated.get("review_required_dimension_ids"), "StageMetricSummary review_required_dimension_ids")
    _require_string_list(validated.get("evidence_missing_dimension_ids"), "StageMetricSummary evidence_missing_dimension_ids")
    _require_non_empty_string(validated.get("status"), "StageMetricSummary status")
    _require_non_empty_string(validated.get("recorded_at"), "StageMetricSummary recorded_at")
    return validated


def validate_workflow_business_review(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, WORKFLOW_BUSINESS_REVIEW_REQUIRED_FIELDS, "WorkflowBusinessReview")
    if validated.get("contract_type") != "WorkflowBusinessReview":
        raise ValueError("WorkflowBusinessReview contract_type must equal 'WorkflowBusinessReview'")
    for field in (
        "workflow_review_id",
        "case_id",
        "stage_id",
        "workflow_name",
        "provider_id",
        "adapter_type",
        "lane_id",
        "fallback_policy_id",
        "status",
        "recorded_at",
    ):
        _require_non_empty_string(validated.get(field), f"WorkflowBusinessReview {field}")
    _require_string_list(validated.get("artifact_refs"), "WorkflowBusinessReview artifact_refs")
    _require_string_list(validated.get("review_questions"), "WorkflowBusinessReview review_questions")
    return validated


def validate_algorithm_benchmark_record(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, ALGORITHM_BENCHMARK_RECORD_REQUIRED_FIELDS, "AlgorithmBenchmarkRecord")
    if validated.get("contract_type") != "AlgorithmBenchmarkRecord":
        raise ValueError("AlgorithmBenchmarkRecord contract_type must equal 'AlgorithmBenchmarkRecord'")
    for field in (
        "benchmark_record_id",
        "case_id",
        "workflow_name",
        "algorithm_surface_id",
        "provider_id",
        "adapter_type",
        "runtime_class",
        "lane_id",
        "fallback_policy_id",
        "status",
        "recorded_at",
    ):
        _require_non_empty_string(validated.get(field), f"AlgorithmBenchmarkRecord {field}")
    _require_string_list(validated.get("artifact_refs"), "AlgorithmBenchmarkRecord artifact_refs")
    _require_string_list(validated.get("benchmark_dimensions"), "AlgorithmBenchmarkRecord benchmark_dimensions")
    return validated


def validate_model_registry_entry(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MODEL_REGISTRY_ENTRY_REQUIRED_FIELDS, "ModelRegistryEntry")
    if validated.get("contract_type") != "ModelRegistryEntry":
        raise ValueError("ModelRegistryEntry contract_type must equal 'ModelRegistryEntry'")
    _require_non_empty_string(validated.get("model_id"), "ModelRegistryEntry model_id")
    _require_non_empty_string(validated.get("provider_id"), "ModelRegistryEntry provider_id")
    _require_non_empty_string(validated.get("display_name"), "ModelRegistryEntry display_name")
    _require_non_empty_string(validated.get("model_family"), "ModelRegistryEntry model_family")
    _require_string_list(validated.get("deployment_modes"), "ModelRegistryEntry deployment_modes")
    _require_string_list(validated.get("capability_tags"), "ModelRegistryEntry capability_tags")
    _require_string_list(validated.get("supported_workflows"), "ModelRegistryEntry supported_workflows")
    _require_non_empty_string(validated.get("status"), "ModelRegistryEntry status")
    return validated


def validate_model_capability_matrix(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MODEL_CAPABILITY_MATRIX_REQUIRED_FIELDS, "ModelCapabilityMatrix")
    if validated.get("contract_type") != "ModelCapabilityMatrix":
        raise ValueError("ModelCapabilityMatrix contract_type must equal 'ModelCapabilityMatrix'")
    _require_non_empty_string(validated.get("matrix_id"), "ModelCapabilityMatrix matrix_id")
    _require_non_empty_string(validated.get("model_id"), "ModelCapabilityMatrix model_id")
    _require_string_list(validated.get("workflow_capabilities"), "ModelCapabilityMatrix workflow_capabilities")
    _require_string_list(validated.get("skill_capabilities"), "ModelCapabilityMatrix skill_capabilities")
    _require_string_list(validated.get("risk_notes"), "ModelCapabilityMatrix risk_notes")
    _require_non_empty_string(validated.get("quality_tier"), "ModelCapabilityMatrix quality_tier")
    return validated


def validate_model_routing_policy(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MODEL_ROUTING_POLICY_REQUIRED_FIELDS, "ModelRoutingPolicy")
    if validated.get("contract_type") != "ModelRoutingPolicy":
        raise ValueError("ModelRoutingPolicy contract_type must equal 'ModelRoutingPolicy'")
    _require_non_empty_string(validated.get("policy_id"), "ModelRoutingPolicy policy_id")
    _require_string_list(validated.get("role_ids"), "ModelRoutingPolicy role_ids")
    _require_string_list(validated.get("lifecycle_stage_ids"), "ModelRoutingPolicy lifecycle_stage_ids")
    _require_non_empty_string(validated.get("preferred_model_id"), "ModelRoutingPolicy preferred_model_id")
    _require_string_list(validated.get("fallback_model_ids"), "ModelRoutingPolicy fallback_model_ids")
    _require_string_list(validated.get("selection_rules"), "ModelRoutingPolicy selection_rules")
    _require_string_list(validated.get("required_capability_tags"), "ModelRoutingPolicy required_capability_tags")
    return validated


def validate_model_eval_summary(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MODEL_EVAL_SUMMARY_REQUIRED_FIELDS, "ModelEvalSummary")
    if validated.get("contract_type") != "ModelEvalSummary":
        raise ValueError("ModelEvalSummary contract_type must equal 'ModelEvalSummary'")
    _require_non_empty_string(validated.get("eval_id"), "ModelEvalSummary eval_id")
    _require_non_empty_string(validated.get("model_id"), "ModelEvalSummary model_id")
    _require_non_empty_string(validated.get("policy_id"), "ModelEvalSummary policy_id")
    _require_non_empty_string(validated.get("evaluation_scope"), "ModelEvalSummary evaluation_scope")
    if not isinstance(validated.get("pass_rate"), (int, float)):
        raise ValueError("ModelEvalSummary pass_rate must be a number")
    _require_string_list(validated.get("known_failure_modes"), "ModelEvalSummary known_failure_modes")
    _require_string_list(validated.get("recommended_for"), "ModelEvalSummary recommended_for")
    return validated


def validate_model_delivery(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, MODEL_DELIVERY_REQUIRED_FIELDS, "ModelDelivery")
    if validated.get("contract_type") != "ModelDelivery":
        raise ValueError("ModelDelivery contract_type must equal 'ModelDelivery'")
    _require_non_empty_string(validated.get("delivery_id"), "ModelDelivery delivery_id")
    _require_non_empty_string(validated.get("case_id"), "ModelDelivery case_id")
    _require_non_empty_string(validated.get("lifecycle_stage_id"), "ModelDelivery lifecycle_stage_id")
    _require_non_empty_string(validated.get("producer_role_profile_id"), "ModelDelivery producer_role_profile_id")
    _require_non_empty_string(validated.get("consumer_lifecycle_stage_id"), "ModelDelivery consumer_lifecycle_stage_id")
    _require_non_empty_string(validated.get("deliverable_kind"), "ModelDelivery deliverable_kind")
    _require_non_empty_string(validated.get("status"), "ModelDelivery status")
    _require_string_list(validated.get("artifact_refs"), "ModelDelivery artifact_refs")
    _require_string_list(validated.get("report_section_refs"), "ModelDelivery report_section_refs")
    return validated


def validate_workflow_report_section(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, WORKFLOW_REPORT_SECTION_REQUIRED_FIELDS, "WorkflowReportSection")
    if validated.get("contract_type") != "WorkflowReportSection":
        raise ValueError("WorkflowReportSection contract_type must equal 'WorkflowReportSection'")
    _require_non_empty_string(validated.get("stage_id"), "WorkflowReportSection stage_id")
    _require_non_empty_string(validated.get("chapter_id"), "WorkflowReportSection chapter_id")
    _require_non_empty_string(validated.get("display_name"), "WorkflowReportSection display_name")
    _require_string_list(validated.get("report_sections"), "WorkflowReportSection report_sections")
    return validated


def validate_agent_network(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, AGENT_NETWORK_REQUIRED_FIELDS, "AgentNetwork")
    if validated.get("contract_type") != "AgentNetwork":
        raise ValueError("AgentNetwork contract_type must equal 'AgentNetwork'")
    _require_non_empty_string(validated.get("case_id"), "AgentNetwork case_id")
    _require_non_empty_string(validated.get("network_id"), "AgentNetwork network_id")
    _require_agent_network_node_list(validated.get("nodes"), "AgentNetwork nodes")
    _require_agent_network_edge_list(validated.get("edges"), "AgentNetwork edges")
    return validated


def validate_tier_message(payload: dict[str, Any]) -> dict[str, Any]:
    validated = _validate_required_fields(payload, TIER_MESSAGE_REQUIRED_FIELDS, "TierMessage")
    if validated.get("contract_type") != "TierMessage":
        raise ValueError("TierMessage contract_type must equal 'TierMessage'")
    _require_non_empty_string(validated.get("message_id"), "TierMessage message_id")
    _require_non_empty_string(validated.get("session_id"), "TierMessage session_id")
    _require_non_empty_string(validated.get("case_id"), "TierMessage case_id")
    _require_non_empty_string(validated.get("message_type"), "TierMessage message_type")
    _require_non_empty_string(validated.get("from_scope"), "TierMessage from_scope")
    _require_non_empty_string(validated.get("to_scope"), "TierMessage to_scope")
    _require_non_empty_string(validated.get("event_type"), "TierMessage event_type")
    _require_non_empty_string(validated.get("recorded_at"), "TierMessage recorded_at")
    return validated
