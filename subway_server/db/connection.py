"""Stub for Team B's PyMySQL setup.

A only ensures the import path exists. Team B fills the implementation.
"""

from typing import Any


def get_connection() -> Any:
    raise NotImplementedError(
        "Team B: implement PyMySQL connection using app.config DB_* values. "
        "Use Flask's `g` object or app.teardown_appcontext for lifecycle."
    )
