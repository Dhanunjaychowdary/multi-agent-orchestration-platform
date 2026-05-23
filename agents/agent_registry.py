"""Agent Registry: Defines and manages all specialized agents."""

import logging
from typing import Dict, Optional
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage
from prompts.system_prompts import (
    RESEARCHER_PROMPT, CODER_PROMPT, ANALYST_PROMPT,
    WRITER_PROMPT, SUMMARIZER_PROMPT, QA_PROMPT,
    GENERAL_PROMPT
)

logger = logging.getLogger(__name__)


class BaseAgent:
      """Base class for all specialized agents."""

    def __init__(self, name: str, system_prompt: str,
                                  model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
                                            self.name = name
                                            self.system_prompt = system_prompt
                                            self.llm = ChatBedrock(
                                                model_id=model_id,
                                                model_kwargs={"max_tokens": 4096, "temperature": 0.3},
                                            )

    def execute(self, query: str) -> str:
              """Execute the agent on a given query."""
              messages = [
                  HumanMessage(content=f"{self.system_prompt}\n\nUser Query: {query}")
              ]
              logger.info(f"[{self.name}] Processing query...")
              response = self.llm.invoke(messages)
              return response.content


class AgentRegistry:
      """Registry for all specialized agents."""

    def __init__(self):
              self.agents: Dict[str, BaseAgent] = {}
              self._register_all()

    def _register_all(self):
              """Register all 7 specialized agents."""
              self.agents = {
                  "researcher": BaseAgent("researcher", RESEARCHER_PROMPT),
                  "coder":      BaseAgent("coder",      CODER_PROMPT),
                  "analyst":    BaseAgent("analyst",    ANALYST_PROMPT),
                  "writer":     BaseAgent("writer",     WRITER_PROMPT),
                  "summarizer": BaseAgent("summarizer", SUMMARIZER_PROMPT),
                  "qa":         BaseAgent("qa",         QA_PROMPT),
                  "general":    BaseAgent("general",    GENERAL_PROMPT),
              }
              logger.info(f"Registered {len(self.agents)} agents: {list(self.agents.keys())}")

    def get_agent(self, name: str) -> Optional[BaseAgent]:
              """Retrieve an agent by name."""
              return self.agents.get(name)

    def list_agents(self) -> list:
              """List all registered agent names."""
              return list(self.agents.keys())
      
