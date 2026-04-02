"""Program-level object contracts for HydroMind workflows and releases.

These dataclasses are intentionally lightweight:
- stdlib only
- JSON-serializable via ``to_dict()``
- stable enough to share across repos
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


PROGRAM_SCHEMA_VERSION = "0.1.0"


@dataclass
class ArtifactRef:
    """Reference to a file, database row, report, or generated artifact."""

    artifact_id: str
    artifact_type: str
    path: str | None = None
    uri: str | None = None
    checksum: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ArtifactRef":
        return cls(
            artifact_id=payload["artifact_id"],
            artifact_type=payload["artifact_type"],
            path=payload.get("path"),
            uri=payload.get("uri"),
            checksum=payload.get("checksum"),
            metadata=dict(payload.get("metadata", {})),
        )


@dataclass
class SourceRecord:
    """One discovered or standardized source item in a case bundle."""

    role: str
    confidence: float
    artifact: ArtifactRef
    evidence: list[str] = field(default_factory=list)
    needs_review: bool = False

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["artifact"] = self.artifact.to_dict()
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceRecord":
        return cls(
            role=payload["role"],
            confidence=float(payload["confidence"]),
            artifact=ArtifactRef.from_dict(payload["artifact"]),
            evidence=list(payload.get("evidence", [])),
            needs_review=bool(payload.get("needs_review", False)),
        )


@dataclass
class CaseManifest:
    """Stable entry object for one case in the HydroMind program."""

    case_id: str
    display_name: str
    raw_root: str
    standard_dataset_id: str | None = None
    priority: str = "normal"
    status: str = "draft"
    owners: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = PROGRAM_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "CaseManifest":
        return cls(
            case_id=payload["case_id"],
            display_name=payload["display_name"],
            raw_root=payload["raw_root"],
            standard_dataset_id=payload.get("standard_dataset_id"),
            priority=payload.get("priority", "normal"),
            status=payload.get("status", "draft"),
            owners=list(payload.get("owners", [])),
            tags=list(payload.get("tags", [])),
            metadata=dict(payload.get("metadata", {})),
            schema_version=payload.get("schema_version", PROGRAM_SCHEMA_VERSION),
        )


@dataclass
class SourceBundle:
    """Normalized bundle of discovered inputs for a case."""

    bundle_id: str
    case_id: str
    records: list[SourceRecord] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    review_required: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = PROGRAM_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "case_id": self.case_id,
            "records": [record.to_dict() for record in self.records],
            "gaps": list(self.gaps),
            "review_required": list(self.review_required),
            "metadata": dict(self.metadata),
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "SourceBundle":
        return cls(
            bundle_id=payload["bundle_id"],
            case_id=payload["case_id"],
            records=[SourceRecord.from_dict(item) for item in payload.get("records", [])],
            gaps=list(payload.get("gaps", [])),
            review_required=list(payload.get("review_required", [])),
            metadata=dict(payload.get("metadata", {})),
            schema_version=payload.get("schema_version", PROGRAM_SCHEMA_VERSION),
        )


@dataclass
class DataPack:
    """Workflow-ready case input package derived from canonical discovery outputs."""

    kind: str = "data_pack"
    case_manifest: str = ""
    source_bundle_json: str = ""
    outlets_json: str = ""
    review_gates: dict[str, str | None] = field(default_factory=dict)
    strict: bool = False
    summary: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = PROGRAM_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "case_manifest": self.case_manifest,
            "source_bundle_json": self.source_bundle_json,
            "outlets_json": self.outlets_json,
            "review_gates": dict(self.review_gates),
            "strict": self.strict,
            "summary": dict(self.summary),
            "metadata": dict(self.metadata),
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "DataPack":
        return cls(
            kind=payload.get("kind", "data_pack"),
            case_manifest=payload.get("case_manifest", ""),
            source_bundle_json=payload.get("source_bundle_json", ""),
            outlets_json=payload.get("outlets_json", ""),
            review_gates=dict(payload.get("review_gates", {})),
            strict=bool(payload.get("strict", False)),
            summary=dict(payload.get("summary", {})),
            metadata=dict(payload.get("metadata", {})),
            schema_version=payload.get("schema_version", PROGRAM_SCHEMA_VERSION),
        )


@dataclass
class WorkflowStepRun:
    """Execution status for one workflow step."""

    step_id: str
    status: str
    inputs: list[ArtifactRef] = field(default_factory=list)
    outputs: list[ArtifactRef] = field(default_factory=list)
    started_at: str | None = None
    completed_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "status": self.status,
            "inputs": [item.to_dict() for item in self.inputs],
            "outputs": [item.to_dict() for item in self.outputs],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WorkflowStepRun":
        return cls(
            step_id=payload["step_id"],
            status=payload["status"],
            inputs=[ArtifactRef.from_dict(item) for item in payload.get("inputs", [])],
            outputs=[ArtifactRef.from_dict(item) for item in payload.get("outputs", [])],
            started_at=payload.get("started_at"),
            completed_at=payload.get("completed_at"),
            metadata=dict(payload.get("metadata", {})),
        )


@dataclass
class WorkflowRun:
    """One execution of a program workflow."""

    run_id: str
    case_id: str
    workflow_type: str
    status: str
    inputs: list[ArtifactRef] = field(default_factory=list)
    outputs: list[ArtifactRef] = field(default_factory=list)
    steps: list[WorkflowStepRun] = field(default_factory=list)
    started_at: str | None = None
    completed_at: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = PROGRAM_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "case_id": self.case_id,
            "workflow_type": self.workflow_type,
            "status": self.status,
            "inputs": [item.to_dict() for item in self.inputs],
            "outputs": [item.to_dict() for item in self.outputs],
            "steps": [step.to_dict() for step in self.steps],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "metadata": dict(self.metadata),
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "WorkflowRun":
        return cls(
            run_id=payload["run_id"],
            case_id=payload["case_id"],
            workflow_type=payload["workflow_type"],
            status=payload["status"],
            inputs=[ArtifactRef.from_dict(item) for item in payload.get("inputs", [])],
            outputs=[ArtifactRef.from_dict(item) for item in payload.get("outputs", [])],
            steps=[WorkflowStepRun.from_dict(item) for item in payload.get("steps", [])],
            started_at=payload.get("started_at"),
            completed_at=payload.get("completed_at"),
            metadata=dict(payload.get("metadata", {})),
            schema_version=payload.get("schema_version", PROGRAM_SCHEMA_VERSION),
        )


@dataclass
class ReviewFinding:
    """One review issue or approval note attached to a run."""

    finding_id: str
    severity: str
    summary: str
    artifact_refs: list[ArtifactRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "summary": self.summary,
            "artifact_refs": [item.to_dict() for item in self.artifact_refs],
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ReviewFinding":
        return cls(
            finding_id=payload["finding_id"],
            severity=payload["severity"],
            summary=payload["summary"],
            artifact_refs=[
                ArtifactRef.from_dict(item) for item in payload.get("artifact_refs", [])
            ],
            metadata=dict(payload.get("metadata", {})),
        )


@dataclass
class ReviewBundle:
    """Human review record for a workflow run."""

    review_id: str
    run_id: str
    case_id: str
    verdict: str
    findings: list[ReviewFinding] = field(default_factory=list)
    report_artifacts: list[ArtifactRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = PROGRAM_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "run_id": self.run_id,
            "case_id": self.case_id,
            "verdict": self.verdict,
            "findings": [item.to_dict() for item in self.findings],
            "report_artifacts": [item.to_dict() for item in self.report_artifacts],
            "metadata": dict(self.metadata),
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ReviewBundle":
        return cls(
            review_id=payload["review_id"],
            run_id=payload["run_id"],
            case_id=payload["case_id"],
            verdict=payload["verdict"],
            findings=[ReviewFinding.from_dict(item) for item in payload.get("findings", [])],
            report_artifacts=[
                ArtifactRef.from_dict(item) for item in payload.get("report_artifacts", [])
            ],
            metadata=dict(payload.get("metadata", {})),
            schema_version=payload.get("schema_version", PROGRAM_SCHEMA_VERSION),
        )


@dataclass
class ReleaseManifest:
    """Published package tying together runs, artifacts, and review outputs."""

    release_id: str
    case_id: str
    version: str
    channel: str
    status: str
    included_runs: list[str] = field(default_factory=list)
    artifacts: list[ArtifactRef] = field(default_factory=list)
    review_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)
    schema_version: str = PROGRAM_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {
            "release_id": self.release_id,
            "case_id": self.case_id,
            "version": self.version,
            "channel": self.channel,
            "status": self.status,
            "included_runs": list(self.included_runs),
            "artifacts": [item.to_dict() for item in self.artifacts],
            "review_refs": list(self.review_refs),
            "metadata": dict(self.metadata),
            "schema_version": self.schema_version,
        }

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "ReleaseManifest":
        return cls(
            release_id=payload["release_id"],
            case_id=payload["case_id"],
            version=payload["version"],
            channel=payload["channel"],
            status=payload["status"],
            included_runs=list(payload.get("included_runs", [])),
            artifacts=[ArtifactRef.from_dict(item) for item in payload.get("artifacts", [])],
            review_refs=list(payload.get("review_refs", [])),
            metadata=dict(payload.get("metadata", {})),
            schema_version=payload.get("schema_version", PROGRAM_SCHEMA_VERSION),
        )
