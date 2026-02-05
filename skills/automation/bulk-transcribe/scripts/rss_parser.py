"""RSS feed parsing for podcast episodes."""

import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request


@dataclass
class Episode:
    """Podcast episode metadata."""
    id: str
    title: str
    audio_url: str
    description: str
    duration: Optional[int] = None  # seconds
    pub_date: Optional[str] = None


def normalize_title(title: str) -> str:
    """Normalize title for use as filename/ID."""
    title = title.lower()
    title = re.sub(r'[^\w\s]', '', title)
    title = '_'.join(title.split())
    return title[:30]


def parse_duration(duration_str: str) -> Optional[int]:
    """Parse duration string to seconds."""
    if not duration_str:
        return None

    # Try HH:MM:SS or MM:SS format
    parts = duration_str.split(':')
    try:
        if len(parts) == 3:
            return int(parts[0]) * 3600 + int(parts[1]) * 60 + int(parts[2])
        elif len(parts) == 2:
            return int(parts[0]) * 60 + int(parts[1])
        else:
            return int(duration_str)
    except (ValueError, TypeError):
        return None


def fetch_rss(url: str) -> str:
    """Fetch RSS feed from URL."""
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urlopen(req, timeout=30) as response:
        return response.read().decode('utf-8')


def parse_feed(source: str) -> tuple[str, list[Episode]]:
    """
    Parse RSS feed from URL or local file.

    Returns: (podcast_title, list of episodes)
    """
    # Determine if URL or file path
    if source.startswith('http://') or source.startswith('https://'):
        xml_content = fetch_rss(source)
        root = ET.fromstring(xml_content)
    else:
        path = Path(source)
        if not path.exists():
            raise FileNotFoundError(f"RSS file not found: {source}")
        tree = ET.parse(path)
        root = tree.getroot()

    # Get podcast title
    channel = root.find('.//channel')
    podcast_title = ""
    if channel is not None:
        title_elem = channel.find('title')
        if title_elem is not None:
            podcast_title = title_elem.text or ""

    # Parse episodes
    episodes = []
    for item in root.findall('.//item'):
        title = item.find('title')
        if title is None or not title.text:
            continue

        title_text = title.text

        # Get audio URL from enclosure
        enclosure = item.find('enclosure')
        if enclosure is None:
            continue

        audio_url = enclosure.get('url')
        audio_type = enclosure.get('type', '')

        if not audio_url:
            continue
        if 'audio' not in audio_type and not audio_url.endswith('.mp3'):
            continue

        # Get description
        description_elem = item.find('description')
        description = ""
        if description_elem is not None and description_elem.text:
            description = description_elem.text[:500]

        # Get duration (try itunes:duration first)
        duration = None
        itunes_duration = item.find('.//{http://www.itunes.com/dtds/podcast-1.0.dtd}duration')
        if itunes_duration is not None and itunes_duration.text:
            duration = parse_duration(itunes_duration.text)

        # Get pub date
        pub_date_elem = item.find('pubDate')
        pub_date = pub_date_elem.text if pub_date_elem is not None else None

        episodes.append(Episode(
            id=normalize_title(title_text),
            title=title_text,
            audio_url=audio_url,
            description=description,
            duration=duration,
            pub_date=pub_date,
        ))

    return podcast_title, episodes


def get_feed_stats(episodes: list[Episode]) -> dict:
    """Calculate statistics about a feed."""
    durations = [e.duration for e in episodes if e.duration]

    return {
        "episode_count": len(episodes),
        "avg_duration_minutes": sum(durations) / len(durations) / 60 if durations else None,
        "total_hours": sum(durations) / 3600 if durations else None,
    }
