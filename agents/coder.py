"""Coder Agent: Handles software engineering, code writing, and debugging tasks."""

import logging
from typing import Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

from prompts.system_prompts import CODER_PROMPT
from tools.code_executor import execute_code

logger = logging.getLogger(__name__)


class CoderAgent:
      """
          Specialized agent for writing code, debugging, code review,
              and technical explanations.
                  """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.name = "coder"
              self.model_id = model_id
              self.system_prompt = CODER_PROMPT
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 8192, "temperature": 0.1},
              )
              logger.info("CoderAgent initialized.")

    def execute(self, query: str, run_code: bool = False) -> str:
              """
                      Execute a coding task.

                              Args:
                                          query: The coding question, task, or code to debug/review.
                                                      run_code: If True and the response contains a Python code block,
                                                                            attempt to execute it and include the output.

                                                                                    Returns:
                                                                                                A code-focused response as a string.
                                                                                                        """
              logger.info("[CoderAgent] Processing query: %s", query[:100])

        full_prompt = (
                      f"{self.system_prompt}\n\n"
                      f"Task: {query}\n\n"
                      "Provide clean, well-commented Python code with type hints. "
                      "Include brief explanations for non-obvious logic."
        )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        result = response.content

        if run_code:
                      code_block = self._extract_python_code(result)
                      if code_block:
                                        exec_result = execute_code(code_block)
                                        if exec_result.get("stdout"):
                                                              result += f"\n\n**Execution Output:**\n```\n{exec_result['stdout']}\n```"
                                                          if exec_result.get("error"):
                                                                                result += f"\n\n**Execution Error:**\n```\n{exec_result['error']}\n```"

                                return result

    def _extract_python_code(self, text: str) -> Optional[str]:
              """Extract the first Python code block from a markdown-formatted string."""
        import re
        pattern = r"```(?:python)?\n(.*?)```"
        match = re.search(pattern, text, re.DOTALL)
        return match.group(1) if match else None

    def review_code(self, code: str) -> str:
              """
                      Perform a code review and return improvement suggestions.

                              Args:
                                          code: Python source code to review.

                                                  Returns:
                                                              Code review feedback as a string.
                                                                      """
        review_prompt = (
                      f"{self.system_prompt}\n\n"
                      f"Please review the following Python code and provide:\n"
                      f"1. A summary of what the code does\n"
                      f"2. Bugs or logical errors found\n"
                      f"3. Style and PEP 8 improvements\n"
                      f"4. Performance optimizations\n"
                      f"5. Security concerns (if any)\n\n"
                      f"Code to review:\n```python\n{code}\n```"
        )
        messages = [HumanMessage(content=review_prompt)]
        response = self.llm.invoke(messages)
        return response.content
