"""Lightweight validators for HydroMind program-level contracts."""

from __future__ import annotations

from typing import Any

from hydromind_contracts.program_contracts import (
    PROGRAM_SCHEMA_VERSION,
    ArtifactRef,
    CaseManifest,
    DataPack,
    ReleaseManifest,
    ReviewBundle,
    ReviewFinding,
    SourceBundle,
    SourceRecord,
    WorkflowRun,
    WorkflowStepRun,
)


def _ensure_schema_version(schema_version: str | None, errors: list[str], label: str) -> None:
    if not schema_version:
        errors.append(f"{label}.schema_version is required")
    elif schema_version != PROGRAM_SCHEMA_VERSION:
        errors.append(
            f"{label}.schema_version must be {PROGRAM_SCHEMA_VERSION!r}, got {schema_version!r}"
        )


def _validate_artifact_ref(artifact: ArtifactRef, label: str, errors: list[str]) -> None:
    if not artifact.artifact_id:
        errors.append(f"{label}.artifact_id is required")
    if not artifact.artifact_type:
        errors.append(f"{label}.artifact_type is required")
    if not artifact.path and not artifact.uri:
        errors.append(f"{label} must define at least one of path or uri")


def _validate_source_record(record: SourceRecord, label: str, errors: list[str]) -> None:
    if not record.role:
        errors.append(f"{label}.role is required")
    if not 0.0 <= record.confidence <= 1.0:
        errors.append(f"{label}.confidence must be between 0 and 1")
    _validate_artifact_ref(record.artifact, f"{label}.artifact", errors)


def _validate_workflow_step(step: WorkflowStepRun, label: str, errors: list[str]) -> None:
    if not step.step_id:
        errors.append(f"{label}.step_id is required")
    if not step.status:
        errors.append(f"{label}.status is required")
    for idx, artifact in enumerate(step.inputs):
        _validate_artifact_ref(artifact, f"{label}.inputs[{idx}]", errors)
    for idx, artifact in enumerate(step.outputs):
        _validate_artifact_ref(artifact, f"{label}.outputs[{idx}]", errors)


def _validate_review_finding(finding: ReviewFinding, label: str, errors: list[str]) -> None:
    if not finding.finding_id:
        errors.append(f"{label}.finding_id is required")
    if not finding.severity:
        errors.append(f"{label}.severity is required")
    if not finding.summary:
        errors.append(f"{label}.summary is required")
    for idx, artifact in enumerate(finding.artifact_refs):
        _validate_artifact_ref(artifact, f"{label}.artifact_refs[{idx}]", errors)


def validate_case_manifest(contract: CaseManifest) -> list[str]:
    errors: list[str] = []
    if not contract.case_id:
        errors.append("case_id is required")
    if not contract.display_name:
        errors.append("display_name is required")
    if not contract.raw_root:
        errors.append("raw_root is required")
    _ensure_schema_version(contract.schema_version, errors, "case_manifest")
    return errors


def validate_source_bundle(contract: SourceBundle) -> list[str]:
    errors: list[str] = []
    if not contract.bundle_id:
        errors.append("bundle_id is required")
    if not contract.case_id:
        errors.append("case_id is required")
    _ensure_schema_version(contract.schema_version, errors, "source_bundle")
    for idx, record in enumerate(contract.records):
        _validate_source_record(record, f"records[{idx}]", errors)
    return errors


def validate_data_pack(contract: DataPack) -> list[str]:
    errors: list[str] = []
    if contract.kind != "data_pack":
        errors.append(f"kind must be 'data_pack', got {contract.kind!r}")
    if not contract.case_manifest:
        errors.append("case_manifest is required")
    if not contract.source_bundle_json:
        errors.append("source_bundle_json is required")
    if not contract.outlets_json:
        errors.append("outlets_json is required")
    review_gates = contract.review_gates
    if not isinstance(review_gates, dict):
        errors.append("review_gates must be a mapping")
    elif contract.strict and not review_gates.get("basin_validation_json"):
        errors.append("strict data_pack requires review_gates.basin_validation_json")
    _ensure_schema_version(contract.schema_version, errors, "data_pack")
    return errors


def validate_workflow_run(contract: WorkflowRun) -> list[str]:
    errors: list[str] = []
    if not contract.run_id:
        errors.append("run_id is required")
    if not contract.case_id:
        errors.append("case_id is required")
    if not contract.workflow_type:
        errors.append("workflow_type is required")
    if not contract.status:
        errors.append("status is required")
    _ensure_schema_version(contract.schema_version, errors, "workflow_run")
    for idx, artifact in enumerate(contract.inputs):
        _validate_artifact_ref(artifact, f"inputs[{idx}]", errors)
    for idx, artifact in enumerate(contract.outputs):
        _validate_artifact_ref(artifact, f"outputs[{idx}]", errors)
    for idx, step in enumerate(contract.steps):
        _validate_workflow_step(step, f"steps[{idx}]", errors)
    return errors


def validate_review_bundle(contract: ReviewBundle) -> list[str]:
    errors: list[str] = []
    if not contract.review_id:
        errors.append("review_id is required")
    if not contract.run_id:
        errors.append("run_id is required")
    if not contract.case_id:
        errors.append("case_id is required")
    if not contract.verdict:
        errors.append("verdict is required")
    _ensure_schema_version(contract.schema_version, errors, "review_bundle")
    for idx, finding in enumerate(contract.findings):
        _validate_review_finding(finding, f"findings[{idx}]", errors)
    for idx, artifact in enumerate(contract.report_artifacts):
        _validate_artifact_ref(artifact, f"report_artifacts[{idx}]", errors)
    return errors


def validate_release_manifest(contract: ReleaseManifest) -> list[str]:
    errors: list[str] = []
    if not contract.release_id:
        errors.append("release_id is required")
    if not contract.case_id:
        errors.append("case_id is required")
    if not contract.version:
        errors.append("version is required")
    if not contract.channel:
        errors.append("channel is required")
    if not contract.status:
        errors.append("status is required")
    _ensure_schema_version(contract.schema_version, errors, "release_manifest")
    for idx, artifact in enumerate(contract.artifacts):
        _validate_artifact_ref(artifact, f"artifacts[{idx}]", errors)
    return errors


def validate_program_contract(contract: Any) -> list[str]:
    if isinstance(contract, CaseManifest):
        return validate_case_manifest(contract)
    if isinstance(contract, SourceBundle):
        return validate_source_bundle(contract)
    if isinstance(contract, DataPack):
        return validate_data_pack(contract)
    if isinstance(contract, WorkflowRun):
        return validate_workflow_run(contract)
    if isinstance(contract, ReviewBundle):
        return validate_review_bundle(contract)
    if isinstance(contract, ReleaseManifest):
        return validate_release_manifest(contract)
    raise TypeError(f"unsupported contract type: {type(contract)!r}")


def load_and_validate_case_manifest(payload: dict[str, Any]) -> tuple[CaseManifest, list[str]]:
    contract = CaseManifest.from_dict(payload)
    return contract, validate_case_manifest(contract)


def load_and_validate_source_bundle(payload: dict[str, Any]) -> tuple[SourceBundle, list[str]]:
    contract = SourceBundle.from_dict(payload)
    return contract, validate_source_bundle(contract)


def load_and_validate_data_pack(payload: dict[str, Any]) -> tuple[DataPack, list[str]]:
    contract = DataPack.from_dict(payload)
    return contract, validate_data_pack(contract)


def load_and_validate_workflow_run(payload: dict[str, Any]) -> tuple[WorkflowRun, list[str]]:
    contract = WorkflowRun.from_dict(payload)
    return contract, validate_workflow_run(contract)


def load_and_validate_review_bundle(payload: dict[str, Any]) -> tuple[ReviewBundle, list[str]]:
    contract = ReviewBundle.from_dict(payload)
    return contract, validate_review_bundle(contract)


def load_and_validate_release_manifest(payload: dict[str, Any]) -> tuple[ReleaseManifest, list[str]]:
    contract = ReleaseManifest.from_dict(payload)
    return contract, validate_release_manifest(contract)


def assert_valid_case_manifest(contract: CaseManifest) -> None:
    errors = validate_case_manifest(contract)
    if errors:
        raise ValueError(errors)


def assert_valid_source_bundle(contract: SourceBundle) -> None:
    errors = validate_source_bundle(contract)
    if errors:
        raise ValueError(errors)


def assert_valid_data_pack(contract: DataPack) -> None:
    errors = validate_data_pack(contract)
    if errors:
        raise ValueError(errors)


def assert_valid_workflow_run(contract: WorkflowRun) -> None:
    errors = validate_workflow_run(contract)
    if errors:
        raise ValueError(errors)


def assert_valid_review_bundle(contract: ReviewBundle) -> None:
    errors = validate_review_bundle(contract)
    if errors:
        raise ValueError(errors)


def assert_valid_release_manifest(contract: ReleaseManifest) -> None:
    errors = validate_release_manifest(contract)
    if errors:
        raise ValueError(errors)
