"""QA Agent: Handles quality assurance, testing strategies, and bug identification."""

import logging
from typing import List, Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

from prompts.system_prompts import QA_PROMPT

logger = logging.getLogger(__name__)


class QAAgent:
    """
    Specialized agent for quality assurance, test case design,
    edge case identification, and code robustness review.
    """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
        self.name = "qa"
        self.model_id = model_id
        self.system_prompt = QA_PROMPT
        self.llm = ChatBedrock(
            model_id=model_id,
            model_kwargs={"max_tokens": 4096, "temperature": 0.2},
        )
        logger.info("QAAgent initialized.")

    def execute(self, query: str) -> str:
        """
        Execute a QA task.

        Args:
            query: The QA question, code/feature to test, or bug report.

        Returns:
            QA analysis, test cases, or bug report as a string.
        """
        logger.info("[QAAgent] Processing query: %s", query[:100])

        full_prompt = (
            f"{self.system_prompt}\n\n"
            f"QA Task: {query}\n\n"
            "Provide a comprehensive QA response including:\n"
            "1. Test strategy overview\n"
            "2. Test cases (happy path + edge cases)\n"
            "3. Potential bugs or failure points\n"
            "4. Recommendations for improvement"
        )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def generate_test_cases(self, function_description: str,
                            num_cases: int = 5) -> str:
        """
        Generate pytest test cases for a described function.

        Args:
            function_description: Natural language description of the function.
            num_cases: Number of test cases to generate.

        Returns:
            Python pytest test code as a string.
        """
        test_prompt = (
            f"{self.system_prompt}\n\n"
            f"Generate {num_cases} pytest test cases for the following function:\n"
            f"{function_description}\n\n"
            "Include: happy path tests, edge cases, error cases. "
            "Use descriptive test function names. Return only valid Python code."
        )
        messages = [HumanMessage(content=test_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def find_bugs(self, code: str) -> str:
        """
        Analyze code and identify potential bugs.

        Args:
            code: Source code to analyze for bugs.

        Returns:
            Bug report with severity levels and fix suggestions.
        """
        bug_prompt = (
            f"{self.system_prompt}\n\n"
            f"Analyze the following code for bugs and issues. "
            f"For each issue found, provide:\n"
            f"- Severity (Critical/High/Medium/Low)\n"
            f"- Location (line number or function name)\n"
            f"- Description of the bug\n"
            f"- Suggested fix\n\n"
            f"Code:\n```python\n{code}\n```"
        )
        messages = [HumanMessage(content=bug_prompt)]
        response = self.llm.invoke(messages)
        return response.content
