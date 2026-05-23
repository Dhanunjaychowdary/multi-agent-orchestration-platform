"""Researcher Agent: Handles information gathering, fact-finding, and research tasks."""

import logging
from typing import Any, Dict, List, Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, SystemMessage

from prompts.system_prompts import RESEARCHER_PROMPT
from tools.web_search import web_search
from tools.summarize import summarize_text

logger = logging.getLogger(__name__)


class ResearcherAgent:
      """
          Specialized agent for research, fact-finding, and information gathering.

              Uses web search to retrieve up-to-date information and summarizes
                  the findings into structured research reports.
                      """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.name = "researcher"
              self.model_id = model_id
              self.system_prompt = RESEARCHER_PROMPT
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 4096, "temperature": 0.2},
              )
              logger.info("ResearcherAgent initialized.")

    def execute(self, query: str, use_web_search: bool = True) -> str:
              """
                      Execute a research task.

                              Args:
                                          query: The research question or topic.
                                                      use_web_search: Whether to attempt a web search first (default True).

                                                              Returns:
                                                                          A structured research response as a string.
                                                                                  """
              logger.info("[ResearcherAgent] Processing query: %s", query[:100])
              context = ""

        if use_web_search:
                      try:
                                        search_results = web_search(query)
                                        if search_results:
                                                              context = f"Web search results:\n{search_results}\n\n"
                                                              logger.info("[ResearcherAgent] Web search completed.")
                      except Exception as exc:  # pylint: disable=broad-except
                          logger.warning("[ResearcherAgent] Web search failed: %s", exc)

                  full_prompt = (
                                f"{self.system_prompt}\n\n"
                                f"{context}"
                                f"Research question: {query}\n\n"
                                "Provide a thorough, well-structured research response with key findings, "
                                "supporting evidence, and a clear conclusion."
                  )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def research_and_summarize(self, topic: str, max_length: int = 500) -> str:
              """
                      Research a topic and return a concise summary.

                              Args:
                                          topic: Topic to research.
                                                      max_length: Approximate target summary length in words.

                                                              Returns:
                                                                          Summarized research findings.
                                                                                  """
              full_research = self.execute(topic)
              try:
                            summary = summarize_text(full_research)
                            return summary
except Exception:  # pylint: disable=broad-except
            # Fallback: truncate the research response
            words = full_research.split()
            return " ".join(words[:max_length]) + ("..." if len(words) > max_length else "")
