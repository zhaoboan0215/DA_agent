# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

from da.storage.fastembed_embeddings import FastEmbedEmbeddings

from .base import BaseEmbeddingStore, StorageBase

__all__ = [
    "BaseEmbeddingStore",
    "StorageBase",
    "FastEmbedEmbeddings",
]
