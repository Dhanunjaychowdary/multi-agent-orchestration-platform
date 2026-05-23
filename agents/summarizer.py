"""Summarizer Agent: Handles document summarization and key point extraction."""

import logging
from typing import Literal, Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

from prompts.system_prompts import SUMMARIZER_PROMPT
from tools.summarize import summarize_text

logger = logging.getLogger(__name__)

SummaryFormat = Literal["paragraph", "bullet_points", "executive_summary", "tldr"]


class SummarizerAgent:
      """
          Specialized agent for condensing long documents into clear summaries,
              extracting key points, and organizing information concisely.
                  """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.name = "summarizer"
              self.model_id = model_id
              self.system_prompt = SUMMARIZER_PROMPT
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 2048, "temperature": 0.1},
              )
              logger.info("SummarizerAgent initialized.")

    def execute(self, query: str,
                                format: SummaryFormat = "paragraph") -> str:
                                          """
                                                  Execute a summarization task.

                                                          Args:
                                                                      query: The text to summarize OR a question about summarization.
                                                                                  format: Output format for the summary.

                                                                                          Returns:
                                                                                                      A concise summary as a string.
                                                                                                              """
                                          logger.info("[SummarizerAgent] Processing query (len=%d).", len(query))

        format_instructions = {
                      "paragraph": "Write the summary as 2-3 concise paragraphs.",
                      "bullet_points": "Use bullet points to list the key points.",
                      "executive_summary": (
                                        "Write an executive summary with: Overview, Key Findings, "
                                        "Implications, and Recommended Actions."
                      ),
                      "tldr": "Write a single TL;DR sentence (max 50 words).",
        }

        fmt_note = format_instructions.get(format, format_instructions["paragraph"])

        full_prompt = (
                      f"{self.system_prompt}\n\n"
                      f"Text to summarize:\n{query}\n\n"
                      f"Summary format: {fmt_note}"
        )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def extract_key_points(self, text: str, max_points: int = 5) -> str:
              """
                      Extract the most important points from a text.

                              Args:
                                          text: Source text.
                                                      max_points: Maximum number of key points to extract.

                                                              Returns:
                                                                          Numbered list of key points as a string.
                                                                                  """
              extract_prompt = (
                  f"{self.system_prompt}\n\n"
                  f"Extract the {max_points} most important points from the text below. "
                  f"Format as a numbered list.\n\n"
                  f"Text:\n{text}"
              )
              messages = [HumanMessage(content=extract_prompt)]
              response = self.llm.invoke(messages)
              return response.content

    def summarize_file_content(self, file_path: str,
                                                              format: SummaryFormat = "paragraph") -> str:
                                                                        """
                                                                                Read a file and summarize its contents.

                                                                                        Args:
                                                                                                    file_path: Path to the file to summarize.
                                                                                                                format: Output format for the summary.
                                                                                                                
                                                                                                                        Returns:
                                                                                                                                    Summary of the file contents.
                                                                                                                                            """
                                                                        from tools.file_reader import read_file
                                                                        content = read_file(file_path)
                                                                        return self.execute(content, format=format)
