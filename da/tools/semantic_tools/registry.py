# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

"""Re-export from DA-semantic-core for backward compatibility."""

from datus_semantic_core.registry import (  # noqa: F401
    AdapterMetadata,
    SemanticAdapterRegistry,
    semantic_adapter_registry,
)

__all__ = ["AdapterMetadata", "SemanticAdapterRegistry", "semantic_adapter_registry"]
