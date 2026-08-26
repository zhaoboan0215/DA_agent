# Copyright 2025-present DAAI, Inc.
# Licensed under the Apache License, Version 2.0.
# See http://www.apache.org/licenses/LICENSE-2.0 for details.

"""
AgentSkills integration for DA-agent.

This module provides skill discovery, loading, and execution capabilities
following the AgentSkills specification (agentskills.io).

Skills are filesystem-based folders containing SKILL.md files with YAML frontmatter
that define specialized capabilities, workflows, and script execution patterns.
"""

from da.tools.skill_tools.skill_bash_tool import SkillBashTool
from da.tools.skill_tools.skill_bundle import calculate_sha256, create_bundle, extract_bundle
from da.tools.skill_tools.skill_config import SkillConfig, SkillMetadata
from da.tools.skill_tools.skill_func_tool import SkillFuncTool
from da.tools.skill_tools.skill_manager import SkillManager
from da.tools.skill_tools.skill_registry import SkillRegistry

__all__ = [
    "SkillConfig",
    "SkillMetadata",
    "SkillRegistry",
    "SkillManager",
    "SkillFuncTool",
    "SkillBashTool",
    "create_bundle",
    "extract_bundle",
    "calculate_sha256",
]
