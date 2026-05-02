from typing import Dict, List

import feedparser


class CollectorAgent:
    """Collects OSINT items from RSS feeds."""

    def collect(self, feeds: List[str], limit: int = 10) -> List[Dict[str, str]]:
        items: List[Dict[str, str]] = []

        for feed_url in feeds:
            parsed = feedparser.parse(feed_url)
            source = parsed.feed.get("title", feed_url)

            for entry in parsed.entries[:limit]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                text = f"{title} {summary}".strip()

                items.append(
                    {
                        "source": source,
                        "text": text,
                    }
                )

        return items[:limit]
