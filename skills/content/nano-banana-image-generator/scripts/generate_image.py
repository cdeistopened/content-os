#!/usr/bin/env python3
"""
Generate and edit images using Gemini API.

Usage:
    # Generate from scratch
    python generate_image.py "Your prompt here"
    python generate_image.py "Your prompt here" --model pro --aspect 16:9

    # Generate with SEO-friendly filename and metadata sidecar
    python generate_image.py "A watercolor illustration of a classroom" \
        --seo-name "classroom-watercolor" \
        --context "Article about project-based learning in homeschools"

    # Edit an existing image (rework mode)
    python generate_image.py "Add snow to the roof" --input ./base-image.png
    python generate_image.py "Change the color to blue" --input ./image.png --model pro

Environment:
    GEMINI_API_KEY or GOOGLE_API_KEY must be set

Requirements:
    pip install google-genai pillow
"""

import argparse
import base64
import json
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai package not installed.")
    print("Install with: pip install google-genai")
    sys.exit(1)

try:
    from PIL import Image
except ImportError:
    print("Error: pillow package not installed.")
    print("Install with: pip install pillow")
    sys.exit(1)


def detect_image_format(data: bytes) -> str:
    """Detect image format from magic bytes.

    Returns 'jpeg', 'png', 'gif', or 'webp'. Defaults to 'jpeg' (Gemini's
    most common output format).
    """
    if data[:8] == b'\x89PNG\r\n\x1a\n':
        return 'png'
    if data[:2] == b'\xff\xd8':
        return 'jpeg'
    if data[:4] == b'GIF8':
        return 'gif'
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP':
        return 'webp'
    return 'jpeg'


FORMAT_EXTENSIONS = {
    'jpeg': '.jpg',
    'png': '.png',
    'gif': '.gif',
    'webp': '.webp',
}


def write_sidecar(image_path: Path, prompt: str, image_format: str,
                  dimensions: tuple, aspect_ratio: str, context: str = None,
                  seo_name: str = None):
    """Write a .meta.json sidecar alongside the saved image."""
    # Build alt text from prompt + context
    alt_parts = []
    if context:
        alt_parts.append(context.split('.')[0].strip())
    # Take first sentence of prompt as fallback
    first_sentence = prompt.split('.')[0].strip()
    if len(first_sentence) < 120:
        alt_parts.append(first_sentence)
    alt_text = ' - '.join(alt_parts) if alt_parts else prompt[:120]

    # Extract keywords from context and prompt
    keywords = []
    source_text = f"{context or ''} {prompt}".lower()
    # Simple keyword extraction: take unique multi-word phrases from context
    if context:
        words = context.lower().split()
        # Take 2-3 word phrases from the context
        for i in range(len(words) - 1):
            phrase = ' '.join(words[i:i+2])
            if len(phrase) > 5 and phrase not in keywords:
                keywords.append(phrase)
                if len(keywords) >= 5:
                    break

    meta = {
        "alt_text": alt_text,
        "keywords": keywords,
        "original_format": image_format,
        "dimensions": {"width": dimensions[0], "height": dimensions[1]},
        "aspect_ratio": aspect_ratio,
        "prompt_summary": prompt[:200],
    }
    if seo_name:
        meta["suggested_seo_name"] = seo_name

    sidecar_path = image_path.with_suffix('.meta.json')
    with open(sidecar_path, 'w') as f:
        json.dump(meta, f, indent=2)
    print(f"Sidecar: {sidecar_path}")


def get_api_key():
    """Get API key from environment."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("Error: No API key found.")
        print("Set GEMINI_API_KEY or GOOGLE_API_KEY environment variable.")
        sys.exit(1)
    return key


def load_image_as_part(image_path: str) -> types.Part:
    """Load an image file and return it as a Gemini Part."""
    path = Path(image_path)
    if not path.exists():
        print(f"Error: Image file not found: {image_path}")
        sys.exit(1)

    # Determine MIME type
    suffix = path.suffix.lower()
    mime_types = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
    }
    mime_type = mime_types.get(suffix, 'image/png')

    # Read and encode image
    with open(path, 'rb') as f:
        image_data = f.read()

    return types.Part.from_bytes(data=image_data, mime_type=mime_type)


def generate_image(
    prompt: str,
    model: str = "pro",
    aspect_ratio: str = "16:9",
    output_dir: str = ".",
    name_prefix: str = None,
    input_image: str = None,
    seo_name: str = None,
    context: str = None,
) -> Path:
    """
    Generate or edit an image.

    Args:
        prompt: The image generation/editing prompt
        model: "flash" or "pro" (pro recommended for editing)
        aspect_ratio: "1:1", "9:16", "16:9", "3:4", "4:3"
        output_dir: Directory to save the image
        name_prefix: Optional prefix for filename
        input_image: Path to reference image for editing (rework mode)
        seo_name: Descriptive SEO filename (e.g. "john-taylor-gatto-education-reformer")
        context: Article title/topic for alt text generation in sidecar

    Returns:
        Path to the saved image
    """
    # Map model names to actual model IDs
    model_id = {
        "flash": "gemini-3-flash-preview",
        "pro": "gemini-3-pro-image-preview"
    }.get(model, model)

    # Initialize client
    client = genai.Client(api_key=get_api_key())

    # Build contents based on whether we have an input image
    if input_image:
        print(f"Rework mode: editing {input_image}")
        image_part = load_image_as_part(input_image)
        contents = [image_part, prompt]
    else:
        contents = [prompt]

    # Configure generation - aspect ratio only supported by pro model
    if model == "pro":
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                aspectRatio=aspect_ratio,
            ),
        )
        if input_image:
            print(f"Editing image with {model_id}...")
        else:
            print(f"Generating with {model_id}...")
        print(f"Aspect ratio: {aspect_ratio}")
    else:
        # Flash model doesn't support aspect ratio config
        config = types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
        )
        if input_image:
            print(f"Editing image with {model_id}...")
        else:
            print(f"Generating with {model_id}...")
        print(f"Note: flash model uses default aspect ratio (include ratio in prompt text)")

    # Generate
    response = client.models.generate_content(
        model=model_id,
        contents=contents,
        config=config,
    )

    # Process response
    output_path = None
    for part in response.parts:
        if part.text is not None:
            print(f"Model response: {part.text}")
        elif part.inline_data is not None:
            # Create output directory
            output_dir = Path(output_dir)
            output_dir.mkdir(parents=True, exist_ok=True)

            # Detect actual image format from raw bytes
            raw_data = part.inline_data.data
            detected_format = detect_image_format(raw_data)
            ext = FORMAT_EXTENSIONS[detected_format]

            # Generate filename
            if seo_name:
                mode_suffix = "edit" if input_image else "gen"
                filename = f"{seo_name}-{mode_suffix}{ext}"
            else:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                prefix = f"{name_prefix}_" if name_prefix else ""
                mode_suffix = "edit" if input_image else "gen"
                filename = f"{prefix}{timestamp}_{mode_suffix}_{model}{ext}"
            output_path = output_dir / filename

            # Save image with correct format
            image = part.as_image()
            image.save(output_path)
            print(f"Saved: {output_path} (detected: {detected_format})")

            # Write metadata sidecar
            # image is a Pydantic Image object, not PIL — open saved file for dimensions
            from PIL import Image as PILImage
            with PILImage.open(output_path) as pil_img:
                width, height = pil_img.size
            write_sidecar(
                image_path=output_path,
                prompt=prompt,
                image_format=detected_format,
                dimensions=(width, height),
                aspect_ratio=aspect_ratio,
                context=context,
                seo_name=seo_name,
            )

    if output_path is None:
        print("Warning: No image was generated in the response.")

    return output_path


def generate_variations(
    prompt: str,
    count: int = 3,
    model: str = "pro",
    aspect_ratio: str = "16:9",
    output_dir: str = ".",
    name_prefix: str = None,
    input_image: str = None,
    seo_name: str = None,
    context: str = None,
) -> list:
    """
    Generate multiple variations of the same prompt/edit.

    Args:
        prompt: The image generation/editing prompt
        count: Number of variations to generate
        model: "flash" or "pro"
        aspect_ratio: Aspect ratio for all images
        output_dir: Directory to save images
        name_prefix: Optional prefix for filenames
        input_image: Path to reference image for editing
        seo_name: Descriptive SEO filename base
        context: Article title/topic for alt text generation

    Returns:
        List of paths to saved images
    """
    paths = []
    for i in range(count):
        print(f"\n--- Variation {i + 1} of {count} ---")
        prefix = f"{name_prefix}_v{i + 1}" if name_prefix else f"v{i + 1}"
        var_seo = f"{seo_name}-v{i + 1}" if seo_name else None
        path = generate_image(
            prompt=prompt,
            model=model,
            aspect_ratio=aspect_ratio,
            output_dir=output_dir,
            name_prefix=prefix,
            input_image=input_image,
            seo_name=var_seo,
            context=context,
        )
        if path:
            paths.append(path)

    return paths


def main():
    parser = argparse.ArgumentParser(
        description="Generate or edit images using Gemini API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Generate from scratch
    python generate_image.py "A paper airplane with dotted trajectory"
    python generate_image.py "A horse with glasses" --model pro --aspect 1:1

    # Edit an existing image (rework mode)
    python generate_image.py "Add snow to the roof" --input ./house.png
    python generate_image.py "Change the background to a beach" --input ./portrait.png
    python generate_image.py "Make the colors more vibrant" --input ./image.png --variations 3
        """,
    )

    parser.add_argument("prompt", help="The image generation or editing prompt")
    parser.add_argument(
        "--input", "-i",
        help="Path to reference image for editing (rework mode)"
    )
    parser.add_argument(
        "--model", "-m",
        choices=["flash", "pro"],
        default="pro",
        help="Model to use: flash (faster) or pro (higher quality, default)"
    )
    parser.add_argument(
        "--aspect", "-a",
        default="16:9",
        help="Aspect ratio: 1:1, 9:16, 16:9, 3:4, 4:3 (default: 16:9)"
    )
    parser.add_argument(
        "--variations", "-v",
        type=int,
        default=1,
        help="Number of variations to generate (default: 1)"
    )
    parser.add_argument(
        "--output", "-o",
        default=".",
        help="Output directory (default: current directory)"
    )
    parser.add_argument(
        "--name", "-n",
        help="Prefix for output filename (legacy, prefer --seo-name)"
    )
    parser.add_argument(
        "--seo-name",
        help="Descriptive SEO filename (e.g. 'john-taylor-gatto-education-reformer')"
    )
    parser.add_argument(
        "--context",
        help="Article title/topic for alt text generation in metadata sidecar"
    )

    args = parser.parse_args()

    if args.variations > 1:
        paths = generate_variations(
            prompt=args.prompt,
            count=args.variations,
            model=args.model,
            aspect_ratio=args.aspect,
            output_dir=args.output,
            name_prefix=args.name,
            input_image=args.input,
            seo_name=args.seo_name,
            context=args.context,
        )
        print(f"\nGenerated {len(paths)} images.")
    else:
        path = generate_image(
            prompt=args.prompt,
            model=args.model,
            aspect_ratio=args.aspect,
            output_dir=args.output,
            name_prefix=args.name,
            input_image=args.input,
            seo_name=args.seo_name,
            context=args.context,
        )
        paths = [path] if path else []

    # Open all generated images in Preview
    if paths:
        print("Opening images in Preview...")
        subprocess.run(["open"] + [str(p) for p in paths])


if __name__ == "__main__":
    main()
