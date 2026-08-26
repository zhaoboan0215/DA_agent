# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

"""
DA-CLI package initialization.
"""

from .autocomplete import SQLCompleter

__all__ = ["DaCLI", "SQLCompleter"]


def __getattr__(name: str):
    """Lazy import to avoid circular dependency with agent modules."""
    if name == "DaCLI":
        from .repl import DaCLI

        return DaCLI
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
