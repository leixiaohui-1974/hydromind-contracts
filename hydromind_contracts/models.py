"""Core contract field definitions for HydroMind."""

CASE_MANIFEST_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "display_name",
    "project_type",
)

WORKFLOW_RUN_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "workflow_name",
    "canonical_workflow_key",
    "run_id",
    "status",
    "inputs",
    "outputs",
    "contracts_emitted",
    "artifacts_emitted",
    "started_at",
    "finished_at",
    "trace_summary",
)

WORKFLOW_RUN_OUTPUT_REQUIRED_FIELDS = (
    "source",
    "terminal_status",
    "artifacts",
    "artifact_records",
    "provider_id",
    "adapter_type",
)

WORKFLOW_RUN_ALLOWED_STATUSES = (
    "planned",
    "running",
    "degraded",
    "blocked",
    "stopped",
    "completed",
    "failed",
)

WORKFLOW_RUN_ALLOWED_SOURCES = (
    "runtime",
    "inferred",
    "inferred_session_terminal",
    "delegated",
)

WORKFLOW_RUN_ALLOWED_ARTIFACT_KINDS = (
    "runtime.directory",
    "runtime.run_summary",
    "runtime.cli_result",
    "runtime.plan",
    "runtime.progress_stream",
    "contract.workflow_run",
    "contract.final_report",
    "artifact.json",
    "artifact.ndjson",
    "artifact.path",
)

WORKFLOW_RUN_ALLOWED_WRITEBACK_KINDS = (
    "writeback.report",
    "writeback.gis",
    "writeback.topology",
    "writeback.parameter",
    "writeback.source",
    "writeback.prompt",
    "writeback.resume",
    "writeback.confirmation",
    "writeback.override",
)

FINAL_REPORT_REQUIRED_FIELDS = (
    "meta",
    "case",
    "readiness",
    "review",
    "release",
    "quality",
    "recommendations",
)

DISPATCH_TOPOLOGY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "topology_id",
    "network_type",
    "corridors",
    "nodes",
    "edges",
)

TARGET_VOLUME_OBJECTIVE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "objective_id",
    "objective_type",
    "target_volume_m3",
    "horizon_hours",
)

TIME_WINDOW_CONSTRAINT_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "constraint_id",
    "horizon_hours",
    "allowed_periods",
)

BOUNDARY_CONDITION_SET_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "condition_set_id",
    "horizon_hours",
    "boundary_conditions",
)

HOURLY_SCHEDULE_RESULT_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "schedule_id",
    "status",
    "horizon_hours",
    "objective_ref",
    "time_window_ref",
    "boundary_condition_ref",
    "timeline",
)

READINESS_BOARD_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "cases",
)

REVIEW_BUNDLE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "review_id",
    "status",
)

RELEASE_MANIFEST_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "release_id",
    "status",
)

PLATFORM_CAPABILITY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "capability_id",
    "display_name",
    "category",
)

EXECUTION_PROVIDER_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "provider_id",
    "display_name",
    "adapter_type",
    "capabilities",
)

HOST_SESSION_BINDING_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "binding_id",
    "platform_id",
    "entry_mode",
    "supports_json",
    "supports_session",
)

TEAM_RUN_STATE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "session_id",
    "status",
    "started_at",
    "updated_at",
)

LIFECYCLE_PHASE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "lifecycle_stage_id",
    "display_name",
    "mission",
    "outputs",
)

MANAGEMENT_LEVEL_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "management_level_id",
    "display_name",
    "scope",
    "responsibilities",
)

ROLE_PROFILE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "role_profile_id",
    "display_name",
    "lifecycle_stage_id",
    "default_management_level_id",
    "workflow_focus",
)

AGENT_NODE_PROFILE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "agent_node_profile_id",
    "display_name",
    "lifecycle_stage_id",
    "management_level_id",
    "role_profile_id",
    "scope_pattern",
)

SESSION_MODE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "agent_session_mode_id",
    "display_name",
    "human_interaction",
)

AGENT_PROFILE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "agent_profile_id",
    "display_name",
    "role_id",
    "role_profile_id",
    "lifecycle_stage_id",
    "management_level_id",
    "default_session_mode_id",
    "supported_skill_ids",
)

SKILL_MANIFEST_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "skill_id",
    "display_name",
    "category",
    "lifecycle_stage_ids",
    "workflow_keys",
    "canonical_workflow_keys",
    "entry_command",
)

AGENT_SKILL_BINDING_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "binding_id",
    "agent_profile_id",
    "skill_id",
    "activation_mode",
)

ROLE_REASONING_SCAFFOLD_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "scaffold_id",
    "role_id",
    "lifecycle_stage_ids",
    "goal_types",
    "required_context_slots",
    "decision_steps",
    "required_evidence",
    "forbidden_shortcuts",
    "handoff_rules",
)

SKILL_EXECUTION_POLICY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "policy_id",
    "skill_id",
    "entry_conditions",
    "required_inputs",
    "execution_steps",
    "preferred_mcp_sequence",
    "fallback_steps",
    "quality_gates",
    "result_schema_expectation",
)

MCP_INVOCATION_POLICY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "policy_id",
    "mcp_group",
    "capability_server_ids",
    "gateway_route_ids",
    "supported_tasks",
    "parameter_templates",
    "invocation_sequence",
    "retry_policy",
    "fallback_policy",
    "trace_requirements",
)

CAPABILITY_MCP_SERVER_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "server_id",
    "display_name",
    "server_kind",
    "transport",
    "tool_ids",
    "supported_task_types",
)

GATEWAY_MCP_ROUTE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "route_id",
    "display_name",
    "gateway_kind",
    "entrypoint",
    "capability_server_ids",
    "supported_workflows",
    "supported_canonical_workflow_keys",
    "invocation_mode",
)

TOOL_INVOCATION_TRACE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "trace_id",
    "case_id",
    "route_id",
    "server_id",
    "tool_name",
    "status",
    "recorded_at",
)

MODEL_REGISTRY_ENTRY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "model_id",
    "provider_id",
    "display_name",
    "model_family",
    "deployment_modes",
    "capability_tags",
    "supported_workflows",
    "status",
)

MODEL_CAPABILITY_MATRIX_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "matrix_id",
    "model_id",
    "workflow_capabilities",
    "skill_capabilities",
    "risk_notes",
    "quality_tier",
)

MODEL_ROUTING_POLICY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "policy_id",
    "role_ids",
    "lifecycle_stage_ids",
    "preferred_model_id",
    "fallback_model_ids",
    "selection_rules",
    "required_capability_tags",
)

MODEL_EVAL_SUMMARY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "eval_id",
    "model_id",
    "policy_id",
    "evaluation_scope",
    "pass_rate",
    "known_failure_modes",
    "recommended_for",
)

EXECUTION_LANE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "lane_id",
    "display_name",
    "provider_id",
    "adapter_type",
    "supported_workflows",
    "supported_canonical_workflow_keys",
    "runtime_class",
    "dispatch_mode",
    "artifact_root_kind",
    "status",
)

FALLBACK_POLICY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "fallback_policy_id",
    "display_name",
    "supported_workflows",
    "supported_canonical_workflow_keys",
    "primary_lane_id",
    "fallback_lane_ids",
    "degrade_mode",
    "retry_budget",
    "terminal_conditions",
)

DISTRIBUTED_TASK_RECEIPT_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "receipt_id",
    "session_id",
    "case_id",
    "workflow_name",
    "canonical_workflow_key",
    "lane_id",
    "fallback_policy_id",
    "provider_id",
    "adapter_type",
    "status",
    "started_at",
    "finished_at",
    "artifact_refs",
)

MODEL_SELECTION_TRACE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "selection_trace_id",
    "session_id",
    "case_id",
    "workflow_name",
    "canonical_workflow_key",
    "role_id",
    "lifecycle_stage_id",
    "policy_id",
    "preferred_model_id",
    "fallback_model_ids",
    "required_model_capability_tags",
    "eval_summary_ids",
    "status",
    "recorded_at",
)

RUNTIME_TELEMETRY_RECORD_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "telemetry_id",
    "session_id",
    "case_id",
    "workflow_name",
    "canonical_workflow_key",
    "status",
    "selection_trace_id",
    "model_policy_id",
    "preferred_model_id",
    "route_ids",
    "server_ids",
    "lane_id",
    "fallback_policy_id",
    "distributed_task_receipt_id",
    "tool_trace_ids",
    "artifact_refs",
    "started_at",
    "finished_at",
)

STAGE_METRIC_SUMMARY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "metric_summary_id",
    "case_id",
    "stage_id",
    "metric_dimensions",
    "covered_dimension_ids",
    "review_required_dimension_ids",
    "evidence_missing_dimension_ids",
    "status",
    "recorded_at",
)

WORKFLOW_BUSINESS_REVIEW_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "workflow_review_id",
    "case_id",
    "stage_id",
    "workflow_name",
    "provider_id",
    "adapter_type",
    "lane_id",
    "fallback_policy_id",
    "artifact_refs",
    "status",
    "review_questions",
    "recorded_at",
)

ALGORITHM_BENCHMARK_RECORD_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "benchmark_record_id",
    "case_id",
    "workflow_name",
    "algorithm_surface_id",
    "provider_id",
    "adapter_type",
    "runtime_class",
    "lane_id",
    "fallback_policy_id",
    "artifact_refs",
    "status",
    "benchmark_dimensions",
    "recorded_at",
)

MODEL_DELIVERY_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "delivery_id",
    "case_id",
    "lifecycle_stage_id",
    "producer_role_profile_id",
    "consumer_lifecycle_stage_id",
    "deliverable_kind",
    "status",
    "artifact_refs",
    "report_section_refs",
)

WORKFLOW_REPORT_SECTION_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "stage_id",
    "chapter_id",
    "display_name",
    "report_sections",
)

AGENT_NETWORK_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "case_id",
    "network_id",
    "nodes",
    "edges",
)

TIER_MESSAGE_REQUIRED_FIELDS = (
    "schema_version",
    "contract_type",
    "message_id",
    "session_id",
    "case_id",
    "message_type",
    "from_scope",
    "to_scope",
    "event_type",
    "recorded_at",
)

CONTRACT_REQUIRED_FIELDS = {
    "CaseManifest": CASE_MANIFEST_REQUIRED_FIELDS,
    "WorkflowRun": WORKFLOW_RUN_REQUIRED_FIELDS,
    "ReviewBundle": REVIEW_BUNDLE_REQUIRED_FIELDS,
    "ReleaseManifest": RELEASE_MANIFEST_REQUIRED_FIELDS,
    "FinalReport": FINAL_REPORT_REQUIRED_FIELDS,
    "DispatchTopology": DISPATCH_TOPOLOGY_REQUIRED_FIELDS,
    "TargetVolumeObjective": TARGET_VOLUME_OBJECTIVE_REQUIRED_FIELDS,
    "TimeWindowConstraint": TIME_WINDOW_CONSTRAINT_REQUIRED_FIELDS,
    "BoundaryConditionSet": BOUNDARY_CONDITION_SET_REQUIRED_FIELDS,
    "HourlyScheduleResult": HOURLY_SCHEDULE_RESULT_REQUIRED_FIELDS,
    "ReadinessBoard": READINESS_BOARD_REQUIRED_FIELDS,
    "PlatformCapability": PLATFORM_CAPABILITY_REQUIRED_FIELDS,
    "ExecutionProvider": EXECUTION_PROVIDER_REQUIRED_FIELDS,
    "HostSessionBinding": HOST_SESSION_BINDING_REQUIRED_FIELDS,
    "TeamRunState": TEAM_RUN_STATE_REQUIRED_FIELDS,
    "LifecyclePhase": LIFECYCLE_PHASE_REQUIRED_FIELDS,
    "ManagementLevel": MANAGEMENT_LEVEL_REQUIRED_FIELDS,
    "RoleProfile": ROLE_PROFILE_REQUIRED_FIELDS,
    "AgentNodeProfile": AGENT_NODE_PROFILE_REQUIRED_FIELDS,
    "SessionMode": SESSION_MODE_REQUIRED_FIELDS,
    "AgentProfile": AGENT_PROFILE_REQUIRED_FIELDS,
    "SkillManifest": SKILL_MANIFEST_REQUIRED_FIELDS,
    "AgentSkillBinding": AGENT_SKILL_BINDING_REQUIRED_FIELDS,
    "RoleReasoningScaffold": ROLE_REASONING_SCAFFOLD_REQUIRED_FIELDS,
    "SkillExecutionPolicy": SKILL_EXECUTION_POLICY_REQUIRED_FIELDS,
    "McpInvocationPolicy": MCP_INVOCATION_POLICY_REQUIRED_FIELDS,
    "CapabilityMcpServer": CAPABILITY_MCP_SERVER_REQUIRED_FIELDS,
    "GatewayMcpRoute": GATEWAY_MCP_ROUTE_REQUIRED_FIELDS,
    "ToolInvocationTrace": TOOL_INVOCATION_TRACE_REQUIRED_FIELDS,
    "ModelRegistryEntry": MODEL_REGISTRY_ENTRY_REQUIRED_FIELDS,
    "ModelCapabilityMatrix": MODEL_CAPABILITY_MATRIX_REQUIRED_FIELDS,
    "ModelRoutingPolicy": MODEL_ROUTING_POLICY_REQUIRED_FIELDS,
    "ModelEvalSummary": MODEL_EVAL_SUMMARY_REQUIRED_FIELDS,
    "ExecutionLane": EXECUTION_LANE_REQUIRED_FIELDS,
    "FallbackPolicy": FALLBACK_POLICY_REQUIRED_FIELDS,
    "DistributedTaskReceipt": DISTRIBUTED_TASK_RECEIPT_REQUIRED_FIELDS,
    "ModelSelectionTrace": MODEL_SELECTION_TRACE_REQUIRED_FIELDS,
    "RuntimeTelemetryRecord": RUNTIME_TELEMETRY_RECORD_REQUIRED_FIELDS,
    "StageMetricSummary": STAGE_METRIC_SUMMARY_REQUIRED_FIELDS,
    "WorkflowBusinessReview": WORKFLOW_BUSINESS_REVIEW_REQUIRED_FIELDS,
    "AlgorithmBenchmarkRecord": ALGORITHM_BENCHMARK_RECORD_REQUIRED_FIELDS,
    "ModelDelivery": MODEL_DELIVERY_REQUIRED_FIELDS,
    "WorkflowReportSection": WORKFLOW_REPORT_SECTION_REQUIRED_FIELDS,
    "AgentNetwork": AGENT_NETWORK_REQUIRED_FIELDS,
    "TierMessage": TIER_MESSAGE_REQUIRED_FIELDS,
}
