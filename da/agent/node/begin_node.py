# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

from typing import AsyncGenerator, Dict, Optional

from da.agent.node import Node
from da.agent.workflow import Workflow
from da.schemas.action_history import ActionHistory, ActionHistoryManager
from da.schemas.base import BaseResult


class BeginNode(Node):
    def update_context(self, workflow: Workflow) -> Dict:
        pass

    def setup_input(self, workflow: Workflow) -> Dict:
        return {"success": True, "message": "Start node, no input needed"}

    def execute(self) -> BaseResult:
        pass

    async def execute_stream(
        self, action_history_manager: Optional[ActionHistoryManager] = None
    ) -> AsyncGenerator[ActionHistory, None]:
        """Begin node has no streaming output, just regular execution."""
        # Begin node doesn't yield any actions
        self.execute()
        return
        yield  # This makes it a generator but never actually yields
