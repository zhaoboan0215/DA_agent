# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

"""Adapter registry with lazy loading for built-in adapters."""

from typing import Dict, List, Type

from da.gateway.channel.base import ChannelAdapter
from da.utils.exceptions import DaException, ErrorCode
from da.utils.loggings import get_logger

logger = get_logger(__name__)

_ADAPTER_TYPES: Dict[str, Type[ChannelAdapter]] = {}


def register_adapter(name: str, cls: Type[ChannelAdapter]) -> None:
    """Register an adapter class under *name*."""
    _ADAPTER_TYPES[name] = cls
    logger.debug("Registered channel adapter: %s -> %s", name, cls.__name__)


def get_adapter_class(name: str) -> Type[ChannelAdapter]:
    """Return the adapter class for *name*, raising ``DaException`` if unknown."""
    if name not in _ADAPTER_TYPES:
        raise DaException(
            ErrorCode.COMMON_UNSUPPORTED,
            message_args={
                "your_value": name,
                "field_name": "channel adapter",
            },
        )
    return _ADAPTER_TYPES[name]


def list_adapters() -> List[str]:
    """Return sorted list of registered adapter names."""
    return sorted(_ADAPTER_TYPES.keys())


def register_builtins() -> None:
    """Lazily import and register built-in adapters."""
    from da.gateway.adapters.feishu import FeishuAdapter
    from da.gateway.adapters.slack import SlackAdapter

    for name, cls in [
        ("feishu", FeishuAdapter),
        ("slack", SlackAdapter),
    ]:
        if name not in _ADAPTER_TYPES:
            register_adapter(name, cls)
