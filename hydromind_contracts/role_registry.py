"""Role module discovery via entry_points for HydroMind.

Role modules are registered under the ``hydromind.roles`` entry-point group.
Each role module provides domain-specific functionality (e.g., water quality
analysis, ice-period management, hydraulic modeling).
"""

from __future__ import annotations

from importlib.metadata import entry_points
from typing import Any

ROLE_GROUP = "hydromind.roles"


def discover_role_modules() -> dict[str, Any]:
    """Discover all registered role module entry points.

    Returns:
        Dictionary mapping role name to its entry-point object.
    """
    eps = entry_points()
    if hasattr(eps, "select"):
        selected = eps.select(group=ROLE_GROUP)
    else:
        selected = eps.get(ROLE_GROUP, [])
    return {ep.name: ep for ep in selected}


def get_role_module(name: str) -> Any:
    """Load and return a role module by name.

    Args:
        name: Role module name as registered in entry points.

    Returns:
        The loaded role module object.

    Raises:
        KeyError: If the requested role module is not registered.
    """
    roles = discover_role_modules()
    if name not in roles:
        raise KeyError(
            f"Role module '{name}' not found. "
            f"Available roles: {sorted(roles.keys())}"
        )
    return roles[name].load()
