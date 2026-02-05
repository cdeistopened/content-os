#!/usr/bin/env python3
"""
Generate videos using Gemini API (Veo 3.1).

Usage:
    python generate_video.py "A cinematic shot of ocean waves at golden hour"
    python generate_video.py "A woman says 'Welcome!' in a bright studio" --model fast
    python generate_video.py "A timelapse of clouds" --duration 8 --resolution 1080p
    python generate_video.py "A cat on a windowsill" --aspect 9:16 --count 2

Environment:
    GEMINI_API_KEY or GOOGLE_API_KEY must be set

Requirements:
    pip install google-genai
"""

import argparse
import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Install with: pip install google-genai")
    sys.exit(1)


def get_api_key():
    """Get API key from environment."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("Error: No API key found.")
        print("Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
        sys.exit(1)
    return key


def generate_video(
    prompt: str,
    model: str = "standard",
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    duration: int = 8,
    negative_prompt: str = None,
    output_dir: str = ".",
    name_prefix: str = None,
    poll_interval: int = 10,
) -> Path:
    """
    Generate a single video from a prompt.

    Args:
        prompt: The video generation prompt (max 1024 tokens)
        model: "standard" (Veo 3.1) or "fast" (Veo 3.1 Fast)
        aspect_ratio: "16:9" or "9:16"
        resolution: "720p", "1080p", or "4k"
        duration: Video length in seconds (4, 6, or 8)
        negative_prompt: Description of unwanted elements
        output_dir: Directory to save the video
        name_prefix: Optional prefix for filename
        poll_interval: Seconds between status checks

    Returns:
        Path to the saved video
    """
    model_id = {
        "standard": "veo-3.1-generate-preview",
        "fast": "veo-3.1-fast-generate-preview",
    }.get(model, model)

    client = genai.Client(api_key=get_api_key())

    print(f"Model: {model_id}")
    print(f"Aspect ratio: {aspect_ratio}")
    print(f"Resolution: {resolution}")
    print(f"Duration: {duration}s")
    if negative_prompt:
        print(f"Negative prompt: {negative_prompt}")
    print(f"Prompt: {prompt[:120]}{'...' if len(prompt) > 120 else ''}")
    print()

    # Build config
    config = types.GenerateVideosConfig(
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        duration_seconds=duration,
        number_of_videos=1,
    )
    if negative_prompt:
        config.negative_prompt = negative_prompt

    # Submit generation request
    print("Submitting video generation request...")
    operation = client.models.generate_videos(
        model=model_id,
        prompt=prompt,
        config=config,
    )

    # Poll until complete
    elapsed = 0
    while not operation.done:
        print(f"  Generating... ({elapsed}s elapsed)")
        time.sleep(poll_interval)
        elapsed += poll_interval
        operation = client.operations.get(operation)

    print(f"Generation complete ({elapsed}s)")

    # Save output
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"{name_prefix}_" if name_prefix else ""
    filename = f"{prefix}{timestamp}_{model}.mp4"
    output_path = output_dir / filename

    generated_video = operation.response.generated_videos[0]
    client.files.download(file=generated_video.video)
    generated_video.video.save(str(output_path))
    print(f"Saved: {output_path}")

    return output_path


def generate_variations(
    prompt: str,
    count: int = 2,
    model: str = "standard",
    aspect_ratio: str = "16:9",
    resolution: str = "720p",
    duration: int = 8,
    negative_prompt: str = None,
    output_dir: str = ".",
    name_prefix: str = None,
) -> list:
    """
    Generate multiple video variations of the same prompt.

    Args:
        prompt: The video generation prompt
        count: Number of variations (1-4)
        model: "standard" or "fast"
        aspect_ratio: "16:9" or "9:16"
        resolution: "720p", "1080p", or "4k"
        duration: Video length in seconds
        negative_prompt: Description of unwanted elements
        output_dir: Directory to save videos
        name_prefix: Optional prefix for filenames

    Returns:
        List of paths to saved videos
    """
    paths = []
    for i in range(count):
        print(f"\n{'='*40}")
        print(f"Variation {i + 1} of {count}")
        print(f"{'='*40}")
        vprefix = f"{name_prefix}_v{i + 1}" if name_prefix else f"v{i + 1}"
        path = generate_video(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            resolution=resolution,
            duration=duration,
            negative_prompt=negative_prompt,
            output_dir=output_dir,
            name_prefix=vprefix,
        )
        if path:
            paths.append(path)
    return paths


def main():
    parser = argparse.ArgumentParser(
        description="Generate videos using Gemini API (Veo 3.1)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python generate_video.py "A cinematic ocean wave at golden hour"
    python generate_video.py "A woman says 'Hello!' in a studio" --model fast
    python generate_video.py "Clouds over mountains" --duration 8 --resolution 1080p
    python generate_video.py "A cat" --aspect 9:16 --count 2 --output ./videos
        """,
    )

    parser.add_argument("prompt", help="The video generation prompt")
    parser.add_argument(
        "--model", "-m",
        choices=["standard", "fast"],
        default="standard",
        help="Model: standard (Veo 3.1, higher quality) or fast (quicker, lower cost)"
    )
    parser.add_argument(
        "--aspect", "-a",
        choices=["16:9", "9:16"],
        default="16:9",
        help="Aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--resolution", "-r",
        choices=["720p", "1080p", "4k"],
        default="720p",
        help="Video resolution (default: 720p)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        choices=[4, 6, 8],
        default=8,
        help="Video duration in seconds (default: 8)"
    )
    parser.add_argument(
        "--negative",
        help="Negative prompt: describe what you DON'T want"
    )
    parser.add_argument(
        "--count", "-c",
        type=int,
        default=1,
        help="Number of variations to generate (default: 1, max: 4)"
    )
    parser.add_argument(
        "--output", "-o",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--name", "-n",
        help="Prefix for output filename"
    )
    parser.add_argument(
        "--poll-interval",
        type=int,
        default=10,
        help="Seconds between status checks (default: 10)"
    )

    args = parser.parse_args()

    if args.count < 1 or args.count > 4:
        print("Error: --count must be between 1 and 4")
        sys.exit(1)

    if args.count > 1:
        paths = generate_variations(
            prompt=args.prompt,
            count=args.count,
            model=args.model,
            aspect_ratio=args.aspect,
            resolution=args.resolution,
            duration=args.duration,
            negative_prompt=args.negative,
            output_dir=args.output,
            name_prefix=args.name,
        )
        print(f"\nGenerated {len(paths)} videos.")
    else:
        generate_video(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect,
            resolution=args.resolution,
            duration=args.duration,
            negative_prompt=args.negative,
            output_dir=args.output,
            name_prefix=args.name,
        )


if __name__ == "__main__":
    main()
