"""Manifest and checkpointing for bulk transcription jobs."""

import csv
import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class EpisodeStatus:
    """Status of a single episode in the job."""
    id: str
    title: str
    status: str  # pending, processing, completed, failed
    input_tokens: int = 0
    output_tokens: int = 0
    input_cost: float = 0.0
    output_cost: float = 0.0
    output_chars: int = 0
    error: Optional[str] = None
    completed_at: Optional[str] = None


@dataclass
class JobConfig:
    """Configuration for a transcription job."""
    feed_url: str
    podcast_name: str
    output_dir: str
    hosts: list[dict] = field(default_factory=list)
    options: dict = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class JobManifest:
    """Manifest tracking a bulk transcription job."""
    config: JobConfig
    episodes: list[EpisodeStatus] = field(default_factory=list)
    total_cost: float = 0.0
    started_at: Optional[str] = None
    completed_at: Optional[str] = None


def save_manifest(manifest: JobManifest, path: Path):
    """Save manifest to JSON file."""
    data = {
        "config": asdict(manifest.config),
        "episodes": [asdict(e) for e in manifest.episodes],
        "total_cost": manifest.total_cost,
        "started_at": manifest.started_at,
        "completed_at": manifest.completed_at,
    }
    path.write_text(json.dumps(data, indent=2))


def load_manifest(path: Path) -> JobManifest:
    """Load manifest from JSON file."""
    data = json.loads(path.read_text())

    config = JobConfig(**data["config"])
    episodes = [EpisodeStatus(**e) for e in data["episodes"]]

    return JobManifest(
        config=config,
        episodes=episodes,
        total_cost=data.get("total_cost", 0.0),
        started_at=data.get("started_at"),
        completed_at=data.get("completed_at"),
    )


def get_pending_episodes(manifest: JobManifest) -> list[EpisodeStatus]:
    """Get episodes that haven't been processed yet."""
    return [e for e in manifest.episodes if e.status == "pending"]


def get_completed_episodes(manifest: JobManifest) -> list[EpisodeStatus]:
    """Get successfully completed episodes."""
    return [e for e in manifest.episodes if e.status == "completed"]


def update_episode_status(
    manifest: JobManifest,
    episode_id: str,
    status: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    input_cost: float = 0.0,
    output_cost: float = 0.0,
    output_chars: int = 0,
    error: Optional[str] = None,
):
    """Update status of an episode in the manifest."""
    for episode in manifest.episodes:
        if episode.id == episode_id:
            episode.status = status
            episode.input_tokens = input_tokens
            episode.output_tokens = output_tokens
            episode.input_cost = input_cost
            episode.output_cost = output_cost
            episode.output_chars = output_chars
            episode.error = error
            if status == "completed":
                episode.completed_at = datetime.now().isoformat()
            break

    # Update total cost
    manifest.total_cost = sum(e.input_cost + e.output_cost for e in manifest.episodes)


def export_cost_csv(manifest: JobManifest, path: Path):
    """Export cost breakdown to CSV."""
    with open(path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            "episode_id", "title", "status",
            "input_tokens", "output_tokens", "output_chars",
            "input_cost", "output_cost", "total_cost"
        ])

        for episode in manifest.episodes:
            total = episode.input_cost + episode.output_cost
            writer.writerow([
                episode.id,
                episode.title[:50],
                episode.status,
                episode.input_tokens,
                episode.output_tokens,
                episode.output_chars,
                f"{episode.input_cost:.4f}",
                f"{episode.output_cost:.4f}",
                f"{total:.4f}",
            ])


def get_job_stats(manifest: JobManifest) -> dict:
    """Get statistics about the job."""
    completed = get_completed_episodes(manifest)
    pending = get_pending_episodes(manifest)
    failed = [e for e in manifest.episodes if e.status == "failed"]

    return {
        "total_episodes": len(manifest.episodes),
        "completed": len(completed),
        "pending": len(pending),
        "failed": len(failed),
        "progress_pct": len(completed) / len(manifest.episodes) * 100 if manifest.episodes else 0,
        "total_cost": manifest.total_cost,
        "avg_cost_per_episode": manifest.total_cost / len(completed) if completed else 0,
    }
