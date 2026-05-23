"""Tool 1: Web Search — search the web for information."""
import logging
import requests
from bs4 import BeautifulSoup
from typing import Optional

logger = logging.getLogger(__name__)


def web_search(query: str, num_results: int = 5) -> str:
      """Search DuckDuckGo for the given query and return top results."""
      try:
                url = f"https://html.duckduckgo.com/html/?q={requests.utils.quote(query)}"
                headers = {"User-Agent": "Mozilla/5.0 (compatible; MultiAgentBot/1.0)"}
                response = requests.get(url, headers=headers, timeout=10)
                response.raise_for_status()

          soup = BeautifulSoup(response.text, "lxml")
        results = []
        for result in soup.select(".result__body")[:num_results]:
                      title_el = result.select_one(".result__title")
                      snippet_el = result.select_one(".result__snippet")
                      url_el = result.select_one(".result__url")
                      if title_el and snippet_el:
                                        results.append(
                                                              f"Title: {title_el.get_text(strip=True)}\n"
                                                              f"URL: {url_el.get_text(strip=True) if url_el else 'N/A'}\n"
                                                              f"Snippet: {snippet_el.get_text(strip=True)}\n"
                                        )

                  if not results:
                                return f"No results found for query: '{query}'"

        return f"Search results for '{query}':\n\n" + "\n".join(results)

except Exception as e:
        logger.error(f"web_search error: {e}")
        return f"Web search failed: {e}"
