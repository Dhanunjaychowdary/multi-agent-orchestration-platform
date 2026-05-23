"""Tool 3: Text Summarization."""
import logging

logger = logging.getLogger(__name__)


def summarize_text(text: str, max_length: int = 500) -> str:
      """Summarize text by extracting the most important sentences."""
      if not text or not text.strip():
                return "No text provided to summarize."

      sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]

    if not sentences:
              return "Could not parse text into sentences."

    # Score sentences by position and length
    scored = []
    for i, sentence in enumerate(sentences):
              score = len(sentence.split())
              if i == 0:
                            score *= 2  # First sentence gets extra weight
        scored.append((score, sentence))

    scored.sort(key=lambda x: x[0], reverse=True)
    selected = sorted(
              [(i, s) for i, (_, s) in enumerate(scored[:5])],
              key=lambda x: x[0]
    )
    summary = ". ".join(s for _, s in selected) + "."

    if len(summary) > max_length:
              summary = summary[:max_length].rsplit(" ", 1)[0] + "..."

    return summary
