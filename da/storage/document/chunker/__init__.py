# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

"""
Document Chunker Module

Provides chunking strategies for splitting documents into retrievable chunks:
- SemanticChunker: Smart chunking based on document structure
"""

from da.storage.document.chunker.semantic_chunker import SemanticChunker

__all__ = [
    "SemanticChunker",
]
