"""Supervisor Agent: Routes tasks to specialized sub-agents using LangGraph."""

import logging
from typing import Any, Dict, List
from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from .agent_registry import AgentRegistry
from prompts.system_prompts.supervisor_prompt import SUPERVISOR_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


class SupervisorAgent:
      """Supervisor agent that classifies tasks and routes to specialized agents."""

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.model_id = model_id
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 2048, "temperature": 0.1},
              )
              self.registry = AgentRegistry()
              self.graph = self._build_graph()
              logger.info(f"SupervisorAgent initialized with model: {model_id}")

    def _classify_task(self, state: Dict[str, Any]) -> Dict[str, Any]:
              """Classify the incoming query and select the appropriate agent."""
              query = state["query"]
              agent_names = list(self.registry.agents.keys())

        classification_prompt = (
                      f"{SUPERVISOR_SYSTEM_PROMPT}\n\n"
                      f"Available agents: {', '.join(agent_names)}\n"
                      f"User query: {query}\n\n"
                      "Respond with ONLY the agent name to route to."
        )

        messages = [HumanMessage(content=classification_prompt)]
        response = self.llm.invoke(messages)
        selected_agent = response.content.strip().lower()

        # Fallback to general agent if unknown
        if selected_agent not in self.registry.agents:
                      logger.warning(f"Unknown agent '{selected_agent}', falling back to 'general'")
                      selected_agent = "general"

        logger.info(f"Classified query to agent: {selected_agent}")
        return {**state, "selected_agent": selected_agent}

    def _execute_agent(self, state: Dict[str, Any]) -> Dict[str, Any]:
              """Execute the selected specialized agent."""
              selected_agent = state["selected_agent"]
              query = state["query"]

        agent = self.registry.get_agent(selected_agent)
        if not agent:
                      return {**state, "response": f"No agent found for task: {selected_agent}"}

        logger.info(f"Executing agent: {selected_agent}")
        response = agent.execute(query)
        return {**state, "response": response}

    def _build_graph(self) -> StateGraph:
              """Build the LangGraph workflow."""
              graph = StateGraph(dict)
              graph.add_node("classify", self._classify_task)
              graph.add_node("execute", self._execute_agent)
              graph.set_entry_point("classify")
              graph.add_edge("classify", "execute")
              graph.add_edge("execute", END)
              return graph.compile()

    def run(self, query: str) -> str:
              """Run the supervisor agent on a user query."""
              initial_state = {"query": query, "selected_agent": None, "response": None}
              result = self.graph.invoke(initial_state)
              return result.get("response", "No response generated.")
      
