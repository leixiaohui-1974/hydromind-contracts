import pytest

from hydromind_contracts.water_object_report import (
    get_water_object_report_convention,
    get_water_object_report_conventions,
    validate_water_object_report_payload,
)


@pytest.mark.parametrize(
    ("alias", "object_type", "template_id"),
    [
        ("pump", "PumpStation", "pump_station_object_template"),
        ("turbine", "PumpStation", "pump_station_object_template"),
        ("gate", "Gate", "gate_object_template"),
        ("valve", "Gate", "gate_object_template"),
        ("river", "Channel", "channel_object_template"),
        ("canal", "Channel", "channel_object_template"),
        ("reservoir", "Reservoir", "reservoir_object_template"),
        ("lake", "Reservoir", "reservoir_object_template"),
        ("pool", "Reservoir", "reservoir_object_template"),
        ("pipeline", "Pipeline", "pipeline_object_template"),
    ],
)
def test_get_water_object_report_convention_accepts_alias(alias, object_type, template_id):
    convention = get_water_object_report_convention(alias)

    assert convention.object_type == object_type
    assert convention.template_id == template_id


def test_get_water_object_report_conventions_exposes_six_core_types():
    payload = get_water_object_report_conventions()

    assert sorted(payload.keys()) == [
        "Channel",
        "Gate",
        "Pipeline",
        "PumpStation",
        "Reservoir",
        "Watershed",
    ]


def test_validate_water_object_report_payload_requires_object_specific_fields():
    errors = validate_water_object_report_payload(
        {
            "object_id": "s1",
            "object_type": "Reservoir",
            "display_name": "瀑布沟",
            "summary": "样本",
            "location": {"case_id": "daduhe"},
            "status": "available",
        }
    )

    assert "Reservoir.storage_capacity is required" in errors
    assert "Reservoir.normal_level is required" in errors
