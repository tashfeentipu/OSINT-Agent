from typing import Dict, List

import feedparser


class OSINTIngestionService:
    """Fetches and normalizes RSS intelligence sources."""

    def ingest_from_feeds(self, feeds: List[str], limit: int = 10) -> List[Dict[str, str]]:
        normalized: List[Dict[str, str]] = []

        for feed_url in feeds:
            parsed = feedparser.parse(feed_url)
            source = parsed.feed.get("title", feed_url)

            for entry in parsed.entries[:limit]:
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                link = entry.get("link", "")
                published = entry.get("published", "unknown")
                combined = f"{title} {summary}".strip()

                normalized.append(
                    {
                        "title": title,
                        "summary": summary,
                        "link": link,
                        "source": source,
                        "published": published,
                        "text": combined,
                    }
                )

        return normalized[:limit]
