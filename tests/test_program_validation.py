"""Tests for program contract validators."""

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
    assert_valid_source_bundle,
    assert_valid_data_pack,
    load_and_validate_review_bundle,
    validate_case_manifest,
    validate_data_pack,
    validate_program_contract,
    validate_release_manifest,
    validate_source_bundle,
    validate_workflow_run,
)


def test_validate_case_manifest_success() -> None:
    contract = CaseManifest(
        case_id="daduhe",
        display_name="大渡河",
        raw_root="/data/raw/daduhe",
    )
    assert validate_case_manifest(contract) == []


def test_validate_source_bundle_rejects_bad_confidence_and_missing_path_uri() -> None:
    contract = SourceBundle(
        bundle_id="bundle-001",
        case_id="daduhe",
        records=[
            SourceRecord(
                role="dem",
                confidence=1.5,
                artifact=ArtifactRef(
                    artifact_id="dem-001",
                    artifact_type="raster",
                ),
            )
        ],
    )
    errors = validate_source_bundle(contract)
    assert any("confidence" in item for item in errors)
    assert any("path or uri" in item for item in errors)


def test_validate_workflow_run_checks_nested_steps() -> None:
    contract = WorkflowRun(
        run_id="run-001",
        case_id="daduhe",
        workflow_type="watershed_delineation",
        status="completed",
        steps=[
            WorkflowStepRun(
                step_id="",
                status="completed",
            )
        ],
    )
    errors = validate_workflow_run(contract)
    assert any("steps[0].step_id" in item for item in errors)


def test_validate_data_pack_checks_required_paths_and_strict_gate() -> None:
    contract = DataPack(
        strict=True,
        review_gates={},
    )
    errors = validate_data_pack(contract)
    assert any("case_manifest is required" in item for item in errors)
    assert any("source_bundle_json is required" in item for item in errors)
    assert any("outlets_json is required" in item for item in errors)
    assert any("strict data_pack requires review_gates.basin_validation_json" in item for item in errors)


def test_validate_review_and_release_contracts() -> None:
    report = ArtifactRef(
        artifact_id="report-001",
        artifact_type="html_report",
        path="/tmp/report.html",
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
                summary="需要补说明。",
                artifact_refs=[report],
            )
        ],
        report_artifacts=[report],
    )
    assert validate_program_contract(review) == []

    release = ReleaseManifest(
        release_id="release-001",
        case_id="daduhe",
        version="v1.0.0",
        channel="staging",
        status="published",
        artifacts=[report],
    )
    assert validate_release_manifest(release) == []

    data_pack = DataPack(
        case_manifest="/cases/daduhe/contracts/case_manifest.json",
        source_bundle_json="/cases/daduhe/contracts/source_bundle.contract.json",
        outlets_json="/cases/daduhe/contracts/outlets.normalized.json",
    )
    assert validate_program_contract(data_pack) == []


def test_load_and_validate_review_bundle_from_dict() -> None:
    payload = {
        "review_id": "review-001",
        "run_id": "run-001",
        "case_id": "daduhe",
        "verdict": "pass",
        "findings": [],
        "report_artifacts": [],
        "metadata": {},
        "schema_version": "0.1.0",
    }
    review, errors = load_and_validate_review_bundle(payload)
    assert review.review_id == "review-001"
    assert errors == []


def test_assert_valid_source_bundle_raises_on_invalid_contract() -> None:
    contract = SourceBundle(
        bundle_id="bundle-001",
        case_id="daduhe",
        records=[
            SourceRecord(
                role="dem",
                confidence=2.0,
                artifact=ArtifactRef(artifact_id="dem-001", artifact_type="raster"),
            )
        ],
    )
    try:
        assert_valid_source_bundle(contract)
    except ValueError as exc:
        assert "confidence" in str(exc)
    else:
        raise AssertionError("assert_valid_source_bundle should raise for invalid contract")


def test_assert_valid_data_pack_raises_on_invalid_contract() -> None:
    contract = DataPack(kind="not-data-pack")
    try:
        assert_valid_data_pack(contract)
    except ValueError as exc:
        assert "kind must be 'data_pack'" in str(exc)
    else:
        raise AssertionError("assert_valid_data_pack should raise for invalid contract")
