"""Processor module for social media sentiment analysis."""

from typing import Any

from textblob import TextBlob

from app.logger import setup_logger

# Initialize logger
logger = setup_logger(__name__)


def analyze_sentiment(data: dict[str, Any]) -> dict[str, Any]:
    """Analyzes sentiment of a social media message (e.g., tweet, post).

    Args:
        data (dict[str, Any]): Dictionary with a 'content' key containing the text to analyze.

    Returns:
        dict[str, Any]: Original data with 'sentiment_score' and 'sentiment_label' added.

    """
    content = data.get("content")

    if not content:
        logger.warning("No content provided for sentiment analysis.")
        data["sentiment_score"] = None
        data["sentiment_label"] = "unknown"
        return data

    try:
        analysis = TextBlob(content)
        sentiment: Any = analysis.sentiment  # ✅ Fixes Pyright access error
        polarity = sentiment.polarity

        data["sentiment_score"] = polarity
        data["sentiment_label"] = classify_sentiment(polarity)

        logger.info(
            "Social sentiment analysis complete: %.2f (%s)", polarity, data["sentiment_label"]
        )
        return data

    except Exception as e:
        logger.error("Social sentiment analysis failed: %s", e)
        data["sentiment_score"] = None
        data["sentiment_label"] = "error"
        return data


def classify_sentiment(score: float) -> str:
    """Classifies polarity score into sentiment label.

    Args:
        score (float): Polarity score from -1 to 1.

    Returns:
        str: 'positive', 'neutral', or 'negative'

    """
    if score > 0.1:
        return "positive"
    elif score < -0.1:
        return "negative"
    return "neutral"
