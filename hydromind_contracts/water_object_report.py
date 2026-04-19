"""Standard conventions for object-level water system reports."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


WATER_OBJECT_REPORT_SCHEMA_VERSION = "1.0.0"

COMMON_REQUIRED_FIELDS = (
    "object_id",
    "object_type",
    "display_name",
    "summary",
    "location",
    "status",
)

COMMON_OPTIONAL_FIELDS = (
    "description",
    "upstream_ids",
    "downstream_ids",
    "tags",
    "evidence_refs",
    "metadata",
)

COMMON_MARKDOWN_SECTIONS = (
    "overview",
    "topology_context",
    "key_parameters",
    "process_and_method",
    "results_and_risks",
    "recommendations_and_evidence",
)

COMMON_JSON_SECTIONS = (
    "summary",
    "object_profile",
    "parameters",
    "metrics",
    "findings",
    "recommendations",
    "evidence",
)


@dataclass(frozen=True)
class WaterObjectReportConvention:
    object_type: str
    display_name: str
    template_id: str
    schema_definition: str
    required_fields: tuple[str, ...]
    optional_fields: tuple[str, ...]
    markdown_sections: tuple[str, ...]
    json_sections: tuple[str, ...]
    aliases: tuple[str, ...] = ()
    compatibility_notes: tuple[str, ...] = ()
    schema_version: str = WATER_OBJECT_REPORT_SCHEMA_VERSION

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _build_convention(
    *,
    object_type: str,
    display_name: str,
    template_id: str,
    required_fields: tuple[str, ...],
    optional_fields: tuple[str, ...],
    aliases: tuple[str, ...] = (),
    compatibility_notes: tuple[str, ...] = (),
) -> WaterObjectReportConvention:
    return WaterObjectReportConvention(
        object_type=object_type,
        display_name=display_name,
        template_id=template_id,
        schema_definition=f"hydromind.water_object_report.{object_type.lower()}@{WATER_OBJECT_REPORT_SCHEMA_VERSION}",
        required_fields=(*COMMON_REQUIRED_FIELDS, *required_fields),
        optional_fields=(*COMMON_OPTIONAL_FIELDS, *optional_fields),
        markdown_sections=COMMON_MARKDOWN_SECTIONS,
        json_sections=COMMON_JSON_SECTIONS,
        aliases=aliases,
        compatibility_notes=compatibility_notes,
    )


WATER_OBJECT_REPORT_CONVENTIONS: dict[str, WaterObjectReportConvention] = {
    "Reservoir": _build_convention(
        object_type="Reservoir",
        display_name="Reservoir",
        template_id="reservoir_object_template",
        required_fields=(
            "storage_capacity",
            "normal_level",
            "flood_limit_level",
            "inflow_design",
            "outlet_structures",
        ),
        optional_fields=(
            "dead_level",
            "operating_rule_curve",
            "sediment_storage",
            "catchment_area_km2",
            "power_capacity_mw",
        ),
        aliases=("reservoir", "res", "water_reservoir", "lake", "pool"),
        compatibility_notes=(
            "Legacy stage-storage metadata should be mapped into operating_rule_curve or storage_capacity.",
            "Missing optional power fields must not block report generation.",
        ),
    ),
    "Channel": _build_convention(
        object_type="Channel",
        display_name="Channel",
        template_id="channel_object_template",
        required_fields=(
            "start_node_id",
            "end_node_id",
            "length_m",
            "design_discharge",
            "roughness",
            "cross_section_profile",
        ),
        optional_fields=(
            "slope",
            "lining_type",
            "bed_elevation_profile",
            "control_points",
            "travel_time_hours",
        ),
        aliases=("channel", "canal", "reach", "river"),
        compatibility_notes=(
            "Legacy Manning n fields may be normalized into roughness.",
            "Cross-section references may be file refs or inline summary objects.",
        ),
    ),
    "PumpStation": _build_convention(
        object_type="PumpStation",
        display_name="PumpStation",
        template_id="pump_station_object_template",
        required_fields=(
            "installed_flow_capacity",
            "pump_unit_count",
            "design_head",
        ),
        optional_fields=(
            "power_supply_mode",
            "discharge_destination",
            "suction_source",
            "performance_curve_ref",
            "standby_units",
            "min_start_stop_interval_min",
            "control_strategy",
        ),
        aliases=("pumpstation", "pump_station", "pump", "station_pump", "turbine"),
        compatibility_notes=(
            "Legacy pump templates can be upgraded by mapping pump_template to pump_station_object_template.",
            "Optional efficiency or performance curves may stay as evidence refs when raw data is external.",
            "Power supply mode and discharge destination are optional until an authoritative structured equipment contract is attached.",
        ),
    ),
    "Gate": _build_convention(
        object_type="Gate",
        display_name="Gate",
        template_id="gate_object_template",
        required_fields=(
            "gate_count",
            "gate_type",
            "sill_elevation",
            "gate_width",
            "operating_rule",
        ),
        optional_fields=(
            "design_head",
            "hoist_type",
            "redundancy_mode",
            "opening_range",
            "safety_interlocks",
        ),
        aliases=("gate", "sluice", "sluice_gate", "valve"),
        compatibility_notes=(
            "Operating curves may be summarized inline when original control tables are unavailable.",
        ),
    ),
    "Pipeline": _build_convention(
        object_type="Pipeline",
        display_name="Pipeline",
        template_id="pipeline_object_template",
        required_fields=(
            "start_node_id",
            "end_node_id",
            "length_m",
            "diameter_m",
            "design_pressure",
        ),
        optional_fields=(
            "material",
            "wall_thickness_mm",
            "roughness",
            "burial_depth_m",
            "pump_booster_refs",
            "valve_refs",
        ),
        aliases=("pipeline", "pipe", "conduit"),
        compatibility_notes=(
            "Legacy diameter values in millimeters should be normalized into diameter_m before publishing.",
            "Pipeline material is optional until authoritative structured design-material contracts are attached.",
        ),
    ),
    "Watershed": _build_convention(
        object_type="Watershed",
        display_name="Watershed",
        template_id="watershed_object_template",
        required_fields=(
            "area_km2",
            "outlet_id",
            "runoff_model",
            "concentration_time_hours",
            "land_use_profile",
        ),
        optional_fields=(
            "mean_slope",
            "soil_profile",
            "rainfall_stations",
            "curve_number",
            "subbasin_count",
        ),
        aliases=("watershed", "basin", "catchment"),
        compatibility_notes=(
            "Legacy catchment outputs should map into Watershed without changing upstream discovery artifacts.",
            "Optional subbasin breakdown can remain sparse while the basin-level summary is complete.",
        ),
    ),
}


def _normalize_object_type(value: str) -> str:
    return "".join(ch for ch in value.strip().lower() if ch.isalnum())


_OBJECT_TYPE_ALIASES: dict[str, str] = {}
for _canonical_name, _convention in WATER_OBJECT_REPORT_CONVENTIONS.items():
    _OBJECT_TYPE_ALIASES[_normalize_object_type(_canonical_name)] = _canonical_name
    for _alias in _convention.aliases:
        _OBJECT_TYPE_ALIASES[_normalize_object_type(_alias)] = _canonical_name


def get_water_object_report_convention(object_type: str) -> WaterObjectReportConvention:
    canonical = _OBJECT_TYPE_ALIASES.get(_normalize_object_type(object_type or ""))
    if not canonical:
        raise KeyError(f"unknown water object report type: {object_type!r}")
    return WATER_OBJECT_REPORT_CONVENTIONS[canonical]


def get_water_object_report_conventions() -> dict[str, WaterObjectReportConvention]:
    return dict(WATER_OBJECT_REPORT_CONVENTIONS)


def validate_water_object_report_payload(payload: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(payload, dict):
        return ["payload must be an object"]

    raw_object_type = str(payload.get("object_type", "")).strip()
    if not raw_object_type:
        return ["object_type is required"]

    try:
        convention = get_water_object_report_convention(raw_object_type)
    except KeyError as exc:
        return [str(exc)]

    for field_name in convention.required_fields:
        value = payload.get(field_name)
        if value is None:
            errors.append(f"{convention.object_type}.{field_name} is required")
            continue
        if isinstance(value, str) and not value.strip():
            errors.append(f"{convention.object_type}.{field_name} must not be empty")

    metadata = payload.get("metadata")
    if metadata is not None and not isinstance(metadata, dict):
        errors.append("metadata must be an object when present")

    evidence_refs = payload.get("evidence_refs")
    if evidence_refs is not None and not isinstance(evidence_refs, list):
        errors.append("evidence_refs must be a list when present")

    sections = payload.get("sections")
    if sections is not None and not isinstance(sections, dict):
        errors.append("sections must be an object when present")

    return errors
