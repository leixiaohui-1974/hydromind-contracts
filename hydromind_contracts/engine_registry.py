"""Engine discovery via entry_points for HydroMind.

Engines are registered under the ``hydromind.engines`` entry-point group.
The registry respects the ``HYDROMIND_ENGINE`` environment variable to allow
deployment-time engine selection without code changes.
"""

from __future__ import annotations

import os
from importlib.metadata import entry_points
from typing import Any

ENGINE_GROUP = "hydromind.engines"


def discover_engines() -> dict[str, Any]:
    """Discover all registered engine entry points.

    Returns:
        Dictionary mapping engine name to its entry-point object.
    """
    eps = entry_points()
    # Python 3.12+ returns a SelectableGroups; 3.9-3.11 returns a dict.
    if hasattr(eps, "select"):
        selected = eps.select(group=ENGINE_GROUP)
    else:
        selected = eps.get(ENGINE_GROUP, [])
    return {ep.name: ep for ep in selected}


def get_engine(name: str | None = None) -> Any:
    """Load and return an engine by name.

    Resolution order:
        1. ``HYDROMIND_ENGINE`` environment variable (if set).
        2. *name* parameter (if provided).
        3. Falls back to ``"builtin"``.

    Args:
        name: Explicit engine name. Overridden by the env var.

    Returns:
        The loaded engine object (whatever the entry point references).

    Raises:
        KeyError: If the requested engine is not registered.
    """
    resolved = os.environ.get("HYDROMIND_ENGINE") or name or "builtin"
    engines = discover_engines()
    if resolved not in engines:
        raise KeyError(
            f"Engine '{resolved}' not found. "
            f"Available engines: {sorted(engines.keys())}"
        )
    return engines[resolved].load()
