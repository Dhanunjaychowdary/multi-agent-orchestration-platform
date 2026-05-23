"""General Agent: Handles miscellaneous tasks that don't fit specialized categories."""

import logging
from typing import Any, Dict, List, Optional

from langchain_aws import ChatBedrock
from langchain.schema import HumanMessage, AIMessage

from prompts.system_prompts import GENERAL_PROMPT

logger = logging.getLogger(__name__)


class GeneralAgent:
      """
          General-purpose agent for answering questions and handling tasks
              that don't fit any of the specialized agent categories.

                  Maintains an optional conversation history for multi-turn interactions.
                      """

    def __init__(self, model_id: str = "anthropic.claude-3-sonnet-20240229-v1:0"):
              self.name = "general"
              self.model_id = model_id
              self.system_prompt = GENERAL_PROMPT
              self.llm = ChatBedrock(
                  model_id=model_id,
                  model_kwargs={"max_tokens": 4096, "temperature": 0.5},
              )
              self._conversation_history: List[Dict[str, str]] = []
              logger.info("GeneralAgent initialized.")

    def execute(self, query: str,
                                session_id: Optional[str] = None) -> str:
                                          """
                                                  Execute a general task.

                                                          Args:
                                                                      query: The user's question or request.
                                                                                  session_id: Optional session ID for conversation continuity.

                                                                                          Returns:
                                                                                                      A helpful, well-organized response as a string.
                                                                                                              """
                                          logger.info("[GeneralAgent] Processing query: %s", query[:100])

        full_prompt = (
                      f"{self.system_prompt}\n\n"
                      f"User request: {query}\n\n"
                      "Provide a clear, accurate, and helpful response."
        )

        messages = [HumanMessage(content=full_prompt)]
        response = self.llm.invoke(messages)
        return response.content

    def chat(self, user_message: str) -> str:
              """
                      Multi-turn conversational interface.

                              Maintains conversation history for the current session.

                                      Args:
                                                  user_message: The user's message.

                                                          Returns:
                                                                      The agent's reply as a string.
                                                                              """
              # Build message list from history
              history_messages = []
              for turn in self._conversation_history:
                            if turn["role"] == "user":
                                              history_messages.append(HumanMessage(content=turn["content"]))
else:
                history_messages.append(AIMessage(content=turn["content"]))

        history_messages.append(
                      HumanMessage(content=f"{self.system_prompt}\n\nUser: {user_message}")
        )

        response = self.llm.invoke(history_messages)
        reply = response.content

        # Update history
        self._conversation_history.append({"role": "user", "content": user_message})
        self._conversation_history.append({"role": "assistant", "content": reply})

        return reply

    def reset_conversation(self) -> None:
              """Clear the conversation history."""
              self._conversation_history = []
              logger.info("[GeneralAgent] Conversation history cleared.")
