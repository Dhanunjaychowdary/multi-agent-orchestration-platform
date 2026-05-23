"""Tool Registry: Manages 6 extensible Python tool APIs."""

import logging
from typing import Any, Dict, Optional
from .web_search import web_search
from .data_retrieval import data_retrieval
from .summarize import summarize_text
from .code_executor import execute_code
from .calculator import calculate
from .file_reader import read_file

logger = logging.getLogger(__name__)


TOOL_REGISTRY: Dict[str, Any] = {
      "web_search": {
                "fn": web_search,
                "description": "Search the web for information on a given topic.",
                "params": {"query": "str"},
      },
      "data_retrieval": {
                "fn": data_retrieval,
                "description": "Retrieve structured data from a given URL or source.",
                "params": {"source": "str", "format": "str"},
      },
      "summarize_text": {
                "fn": summarize_text,
                "description": "Summarize a long piece of text.",
                "params": {"text": "str", "max_length": "int"},
      },
      "execute_code": {
                "fn": execute_code,
                "description": "Safely execute a snippet of Python code and return the output.",
                "params": {"code": "str"},
      },
      "calculate": {
                "fn": calculate,
                "description": "Evaluate a mathematical expression and return the result.",
                "params": {"expression": "str"},
      },
      "read_file": {
                "fn": read_file,
                "description": "Read the contents of a local file.",
                "params": {"file_path": "str"},
      },
}


def get_tool(name: str) -> Optional[Dict[str, Any]]:
      """Retrieve a tool by name."""
      tool = TOOL_REGISTRY.get(name)
      if not tool:
                logger.warning(f"Tool '{name}' not found in registry.")
            return tool


def run_tool(name: str, **kwargs) -> Any:
      """Run a tool by name with given keyword arguments."""
    tool = get_tool(name)
    if not tool:
              return f"Error: Tool '{name}' not found."
          try:
                    logger.info(f"Running tool: {name} with args: {list(kwargs.keys())}")
                    return tool["fn"](**kwargs)
except Exception as e:
        logger.error(f"Tool '{name}' failed: {e}")
        return f"Tool error: {e}"


def list_tools() -> list:
      """List all available tool names."""
    return list(TOOL_REGISTRY.keys())
