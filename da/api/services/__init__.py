"""API Services module.

Consolidated service layer for Da Agent API.
"""

# Core services
from da.api.services.da_service_cache import DaServiceCache

# Lazy imports - services are imported only when needed by routes
# This avoids circular dependencies and import errors

__all__ = [
    "DaServiceCache",
]


def __getattr__(name):
    """Lazy import of services on demand."""
    if name == "DaService":
        from da.api.services.da_service import DaService

        return DaService
    elif name == "ChatService":
        from da.api.services.chat_service import ChatService

        return ChatService
    elif name == "ChatTaskManager":
        from da.api.services.chat_task_manager import ChatTaskManager

        return ChatTaskManager
    elif name == "ChatTask":
        from da.api.services.chat_task_manager import ChatTask

        return ChatTask
    elif name == "CLIService":
        from da.api.services.cli_service import CLIService

        return CLIService
    elif name == "DatasourceService":
        from da.api.services.database_service import DatasourceService

        return DatasourceService
    elif name == "ExplorerService":
        from da.api.services.explorer_service import ExplorerService

        return ExplorerService
    elif name == "MCPService":
        from da.api.services.mcp_service import MCPService

        return MCPService
    elif name == "KbService":
        from da.api.services.kb_service import KbService

        return KbService
    elif name == "action_to_sse_event":
        from da.api.services.action_sse_converter import action_to_sse_event

        return action_to_sse_event
    elif name == "AgentService":
        from da.api.services.agent_service import AgentService

        return AgentService
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
