"""Analyst Agent: Handles data analysis, statistics, and insight generation."""

import logging
from typing import Any, Dict, List, Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

from prompts.system_prompts import ANALYST_PROMPT
from tools.calculator import calculate

logger = logging.getLogger(__name__)


class AnalystAgent:
      """
          Specialized agent for data analysis, statistical reasoning,
              trend identification, and generating actionable insights.
                  """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.name = "analyst"
              self.model_id = model_id
              self.system_prompt = ANALYST_PROMPT
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 4096, "temperature": 0.2},
              )
              logger.info("AnalystAgent initialized.")

    def execute(self, query: str, data: Optional[str] = None) -> str:
              """
                      Execute a data analysis task.

                              Args:
                                          query: The analysis question or task description.
                                                      data: Optional raw data to analyze (CSV snippet, JSON, text table, etc.).

                                                              Returns:
                                                                          A structured analytical report as a string.
                                                                                  """
              logger.info("[AnalystAgent] Processing query: %s", query[:100])

        data_section = f"\n\nData provided:\n{data}" if data else ""

        full_prompt = (
                      f"{self.system_prompt}\n\n"
                      f"Analysis task: {query}"
                      f"{data_section}\n\n"
                      "Provide a structured analytical report with:\n"
                      "1. Key observations and patterns\n"
                      "2. Statistical insights (where applicable)\n"
                      "3. Interpretation of trends\n"
                      "4. Actionable recommendations\n"
                      "5. Limitations or caveats"
        )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def calculate_and_analyze(self, expression: str, context: str = "") -> str:
              """
                      Perform a calculation and provide analytical context.

                              Args:
                                          expression: Mathematical expression to evaluate.
                                                      context: Optional context to interpret the result.

                                                              Returns:
                                                                          Calculation result with analytical commentary.
                                                                                  """
              try:
                            result = calculate(expression)
                            calc_context = f"Calculation: {expression} = {result}"
                            if context:
                                              calc_context += f"\nContext: {context}"
                                          return self.execute(f"Interpret this result: {calc_context}")
except Exception as exc:  # pylint: disable=broad-except
            logger.error("[AnalystAgent] Calculation failed: %s", exc)
            return f"Calculation error: {exc}"
