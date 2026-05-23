"""Tool 2: Data Retrieval — fetch data from URLs or APIs."""
import logging
import requests
import json
from typing import Optional

logger = logging.getLogger(__name__)


def data_retrieval(source: str, format: str = "json") -> str:
      """Fetch data from a URL. Supports JSON and raw text."""
      try:
                headers = {"User-Agent": "Mozilla/5.0 (compatible; MultiAgentBot/1.0)"}
                response = requests.get(source, headers=headers, timeout=15)
                response.raise_for_status()

          if format.lower() == "json":
                        data = response.json()
                        return json.dumps(data, indent=2)[:5000]  # Limit output
else:
            return response.text[:5000]  # Limit output

except requests.exceptions.JSONDecodeError:
        return response.text[:5000]
except Exception as e:
        logger.error(f"data_retrieval error: {e}")
        return f"Data retrieval failed: {e}"
