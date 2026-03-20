from __future__ import annotations

import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_WORKSPACE = REPO_ROOT.parent


def get_workspace_root() -> Path:
    override = os.environ.get("HYDROMIND_WORKSPACE")
    if override:
        return Path(override).resolve()
    return DEFAULT_WORKSPACE


def project_paths() -> dict[str, Path]:
    workspace = get_workspace_root()
    return {
        "HydroGuard": workspace / "HydroGuard",
        "HydroDesign": workspace / "HydroDesign",
        "HydroArena": workspace / "HydroArena",
        "HydroEdu": workspace / "HydroEdu",
        "HydroLab": workspace / "HydroLab",
    }


def add_existing_projects_to_syspath(projects: dict[str, Path]) -> None:
    for path in projects.values():
        if path.exists() and str(path) not in sys.path:
            sys.path.insert(0, str(path))
