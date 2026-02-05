#!/usr/bin/env python3
import argparse
import json
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

from utils import iso_date, load_manifest, slugify, write_manifest, write_text

YOUTUBE_HOSTS = ("youtube.com", "www.youtube.com", "youtu.be")


def is_youtube_url(url: str) -> bool:
    return any(host in url for host in YOUTUBE_HOSTS)


def extract_video_id(url: str) -> str:
    if "youtu.be/" in url:
        return url.split("youtu.be/")[-1].split("?")[0]
    if "v=" in url:
        return url.split("v=")[-1].split("&")[0]
    return ""


def parse_feed(xml_text: str):
    root = ET.fromstring(xml_text)
    channel = root.find("channel")
    if channel is None:
        raise ValueError("Invalid RSS feed: missing channel")

    ns = {
        "itunes": "http://www.itunes.com/dtds/podcast-1.0.dtd",
        "podcast": "https://podcastindex.org/namespace/1.0",
        "media": "http://search.yahoo.com/mrss/",
    }

    title = channel.findtext("title") or "Unknown Show"
    items = []
    for item in channel.findall("item"):
        item_title = item.findtext("title") or "Untitled"
        link = item.findtext("link") or ""
        guid = item.findtext("guid") or ""
        pub_date = item.findtext("pubDate") or ""

        enclosure = item.find("enclosure")
        audio_url = enclosure.get("url") if enclosure is not None else ""

        transcript_url = ""
        transcript_type = ""
        transcript_el = item.find("podcast:transcript", ns)
        if transcript_el is not None:
            transcript_url = transcript_el.get("url", "")
            transcript_type = transcript_el.get("type", "")
        if not transcript_url:
            for tag in ("transcript", "media:transcript"):
                transcript_el = item.find(tag, ns)
                if transcript_el is not None:
                    transcript_url = transcript_el.get("url", "") or (
                        transcript_el.text or ""
                    )
                    transcript_type = transcript_el.get("type", "")
                    break

        item_id = guid or extract_video_id(link) or slugify(item_title)
        items.append(
            {
                "id": item_id,
                "show": title,
                "title": item_title,
                "date": iso_date(pub_date),
                "link": link,
                "audio_url": audio_url or None,
                "transcript_url": transcript_url or None,
                "transcript_type": transcript_type or None,
                "youtube_url": link if link and is_youtube_url(link) else None,
                "video_id": extract_video_id(link) if link else None,
            }
        )

    return title, items


def build_report(items):
    total = len(items)
    audio_count = sum(1 for i in items if i.get("audio_url"))
    transcript_count = sum(1 for i in items if i.get("transcript_url"))
    youtube_count = sum(1 for i in items if i.get("youtube_url"))
    stt_needed = sum(
        1 for i in items if not i.get("transcript_url") and not i.get("youtube_url")
    )
    return {
        "total": total,
        "audio_count": audio_count,
        "transcript_count": transcript_count,
        "youtube_count": youtube_count,
        "stt_needed": stt_needed,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--feed-url", required=True)
    parser.add_argument("--project-root", required=True)
    args = parser.parse_args()

    project_root = Path(args.project_root)
    project_root.mkdir(parents=True, exist_ok=True)
    data_dir = project_root / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    with urllib.request.urlopen(args.feed_url) as resp:
        xml_text = resp.read().decode("utf-8", errors="ignore")

    show_title, items = parse_feed(xml_text)

    manifest_path = data_dir / "manifest.jsonl"
    existing = load_manifest(manifest_path)
    existing_ids = {e.get("id") for e in existing}

    merged = list(existing)
    for item in items:
        if item["id"] in existing_ids:
            continue
        item["status"] = "pending"
        item["notes"] = []
        merged.append(item)

    write_manifest(manifest_path, merged)

    report = build_report(items)
    report["show_title"] = show_title
    write_text(data_dir / "sources_report.json", json.dumps(report, indent=2))

    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
