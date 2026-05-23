"""Writer Agent: Handles content creation, editing, and writing tasks."""

import logging
from typing import Literal, Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage

from prompts.system_prompts import WRITER_PROMPT

logger = logging.getLogger(__name__)

ContentStyle = Literal["formal", "casual", "technical", "creative", "persuasive"]


class WriterAgent:
      """
          Specialized agent for content creation, editing, proofreading,
              and adapting tone for different audiences.
                  """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.name = "writer"
              self.model_id = model_id
              self.system_prompt = WRITER_PROMPT
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 8192, "temperature": 0.7},
              )
              logger.info("WriterAgent initialized.")

    def execute(self, query: str, style: Optional[ContentStyle] = None) -> str:
              """
                      Execute a writing task.

                              Args:
                                          query: The writing request (e.g. "Write a blog post about AI agents").
                                                      style: Optional content style to apply.

                                                              Returns:
                                                                          The generated written content as a string.
                                                                                  """
              logger.info("[WriterAgent] Processing query: %s", query[:100])

        style_note = f"\nWrite in a {style} style." if style else ""

        full_prompt = (
                      f"{self.system_prompt}\n\n"
                      f"Writing task: {query}"
                      f"{style_note}\n\n"
                      "Produce high-quality, engaging, well-structured content."
        )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def edit(self, text: str, instructions: str = "") -> str:
              """
                      Edit and improve an existing piece of text.

                              Args:
                                          text: The text to edit.
                                                      instructions: Specific editing instructions (e.g. "make it more concise").

                                                              Returns:
                                                                          The edited text as a string.
                                                                                  """
              edit_instructions = instructions or "improve clarity, grammar, and flow"
              edit_prompt = (
                  f"{self.system_prompt}\n\n"
                  f"Please edit the following text to {edit_instructions}. "
                  f"Return ONLY the edited text without explanations.\n\n"
                  f"Original text:\n{text}"
              )
              messages = [HumanMessage(content=edit_prompt)]
              response = self.llm.invoke(messages)
              return response.content

    def write_email(self, subject: str, context: str,
                                        tone: ContentStyle = "formal") -> str:
                                                  """
                                                          Write a professional email.

                                                                  Args:
                                                                              subject: Email subject line.
                                                                                          context: Context and key points to include.
                                                                                                      tone: Tone of the email (default 'formal').
                                                                                                      
                                                                                                              Returns:
                                                                                                                          A complete email draft as a string.
                                                                                                                                  """
                                                  email_prompt = (
                                                      f"{self.system_prompt}\n\n"
                                                      f"Write a {tone} email.\n"
                                                      f"Subject: {subject}\n"
                                                      f"Key points to cover: {context}\n\n"
                                                      "Format the output as a complete email with Subject, greeting, body, and sign-off."
                                                  )
                                                  messages = [HumanMessage(content=email_prompt)]
                                                  response = self.llm.invoke(messages)
                                                  return response.content
