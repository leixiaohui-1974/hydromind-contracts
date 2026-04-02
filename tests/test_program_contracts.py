"""Tests for program-level object contracts."""

from hydromind_contracts import (
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


def test_case_manifest_round_trip() -> None:
    manifest = CaseManifest(
        case_id="daduhe",
        display_name="大渡河",
        raw_root="/data/raw/daduhe",
        standard_dataset_id="case_daduhe_v1",
        priority="mvp",
        status="active",
        owners=["program"],
        tags=["hydrology", "mvp"],
        metadata={"crs": "EPSG:4326"},
    )
    restored = CaseManifest.from_dict(manifest.to_dict())
    assert restored == manifest


def test_source_bundle_round_trip() -> None:
    bundle = SourceBundle(
        bundle_id="bundle-001",
        case_id="daduhe",
        records=[
            SourceRecord(
                role="dem",
                confidence=0.98,
                artifact=ArtifactRef(
                    artifact_id="dem-001",
                    artifact_type="raster",
                    path="/data/raw/daduhe/dem.tif",
                ),
                evidence=["filename contains dem", "extent overlaps case bbox"],
            )
        ],
        gaps=["soil_raster"],
        review_required=["rainfall_timeseries"],
    )
    restored = SourceBundle.from_dict(bundle.to_dict())
    assert restored.case_id == "daduhe"
    assert restored.records[0].artifact.path == "/data/raw/daduhe/dem.tif"
    assert restored.gaps == ["soil_raster"]


def test_workflow_run_round_trip() -> None:
    step = WorkflowStepRun(
        step_id="flow-analysis",
        status="completed",
        outputs=[
            ArtifactRef(
                artifact_id="flow-acc-001",
                artifact_type="raster",
                path="/runs/daduhe/flow_acc.tif",
            )
        ],
    )
    run = WorkflowRun(
        run_id="run-001",
        case_id="daduhe",
        workflow_type="watershed_delineation",
        status="completed",
        steps=[step],
    )
    restored = WorkflowRun.from_dict(run.to_dict())
    assert restored.steps[0].step_id == "flow-analysis"
    assert restored.workflow_type == "watershed_delineation"


def test_data_pack_round_trip() -> None:
    contract = DataPack(
        case_manifest="/cases/daduhe/contracts/case_manifest.json",
        source_bundle_json="/cases/daduhe/contracts/source_bundle.contract.json",
        outlets_json="/cases/daduhe/contracts/outlets.normalized.json",
        review_gates={"basin_validation_json": "/cases/daduhe/contracts/basin_validation_report.json"},
        strict=True,
        summary={"outlet_count": 7},
        metadata={"producer": "Hydrology/workflows/build_data_pack.py"},
    )
    restored = DataPack.from_dict(contract.to_dict())
    assert restored.kind == "data_pack"
    assert restored.review_gates["basin_validation_json"].endswith("basin_validation_report.json")
    assert restored.strict is True


def test_review_and_release_round_trip() -> None:
    report_artifact = ArtifactRef(
        artifact_id="report-001",
        artifact_type="html_report",
        path="/reviews/daduhe/report.html",
    )
    review = ReviewBundle(
        review_id="review-001",
        run_id="run-001",
        case_id="daduhe",
        verdict="pass_with_comments",
        findings=[
            ReviewFinding(
                finding_id="finding-001",
                severity="medium",
                summary="峰值低估，需要复查降雨输入。",
                artifact_refs=[report_artifact],
            )
        ],
        report_artifacts=[report_artifact],
    )
    restored_review = ReviewBundle.from_dict(review.to_dict())
    assert restored_review.findings[0].severity == "medium"

    release = ReleaseManifest(
        release_id="release-001",
        case_id="daduhe",
        version="v1.0.0",
        channel="staging",
        status="published",
        included_runs=["run-001"],
        artifacts=[report_artifact],
        review_refs=["review-001"],
    )
    restored_release = ReleaseManifest.from_dict(release.to_dict())
    assert restored_release.artifacts[0].artifact_type == "html_report"
    assert restored_release.review_refs == ["review-001"]
