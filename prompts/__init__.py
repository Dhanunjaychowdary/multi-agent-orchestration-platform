"""Prompts package for multi-agent orchestration platform."""

from prompts.system_prompts import (
    SUPERVISOR_SYSTEM_PROMPT,
    RESEARCHER_SYSTEM_PROMPT,
    CODER_SYSTEM_PROMPT,
    ANALYST_SYSTEM_PROMPT,
    WRITER_SYSTEM_PROMPT,
    SUMMARIZER_SYSTEM_PROMPT,
    QA_SYSTEM_PROMPT,
    GENERAL_SYSTEM_PROMPT,
    get_prompt_for_agent,
)

__all__ = [
      "SUPERVISOR_SYSTEM_PROMPT",
      "RESEARCHER_SYSTEM_PROMPT",
      "CODER_SYSTEM_PROMPT",
      "ANALYST_SYSTEM_PROMPT",
      "WRITER_SYSTEM_PROMPT",
      "SUMMARIZER_SYSTEM_PROMPT",
      "QA_SYSTEM_PROMPT",
      "GENERAL_SYSTEM_PROMPT",
      "get_prompt_for_agent",
]
