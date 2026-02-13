#!/usr/bin/env python3
"""
Convert images to WebP with target dimension presets.

Keeps the original file intact (needed for edit/rework). Updates the
.meta.json sidecar with the WebP path and final dimensions.

Usage:
    python3 image_optimizer.py image.jpg --use thumbnail
    python3 image_optimizer.py image.jpg --use social-square
    python3 image_optimizer.py image.jpg --use inline --quality 80

Presets:
    thumbnail       1200x675  (16:9, Webflow blog)
    social-square   1080x1080
    social-portrait 1080x1350
    inline          max-width 800px, proportional height

Requirements:
    pip install pillow
"""

import argparse
import json
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Error: pillow package not installed.")
    print("Install with: pip install pillow")
    sys.exit(1)


PRESETS = {
    "thumbnail": (1200, 675),
    "social-square": (1080, 1080),
    "social-portrait": (1080, 1350),
    "inline": (800, None),  # None = proportional
}


def optimize_image(
    input_path: str,
    preset: str = "thumbnail",
    quality: int = 85,
    output_dir: str = None,
) -> Path:
    """
    Convert an image to WebP at the given preset dimensions.

    Args:
        input_path: Path to source image
        preset: One of thumbnail, social-square, social-portrait, inline
        quality: WebP quality (1-100, default 85)
        output_dir: Output directory (defaults to same as input)

    Returns:
        Path to the saved WebP file
    """
    src = Path(input_path)
    if not src.exists():
        print(f"Error: File not found: {src}")
        sys.exit(1)

    if preset not in PRESETS:
        print(f"Error: Unknown preset '{preset}'. Choose from: {', '.join(PRESETS)}")
        sys.exit(1)

    target_w, target_h = PRESETS[preset]
    img = Image.open(src)

    # Convert RGBA to RGB for WebP compatibility (avoid transparency issues)
    if img.mode == 'RGBA':
        bg = Image.new('RGB', img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[3])
        img = bg
    elif img.mode != 'RGB':
        img = img.convert('RGB')

    # Resize
    if target_h is None:
        # Proportional: constrain width only
        if img.width > target_w:
            ratio = target_w / img.width
            target_h_calc = int(img.height * ratio)
            img = img.resize((target_w, target_h_calc), Image.LANCZOS)
        # else: leave as-is if already smaller
    else:
        # Exact dimensions: resize to cover, then center-crop
        src_ratio = img.width / img.height
        dst_ratio = target_w / target_h

        if src_ratio > dst_ratio:
            # Source is wider: fit height, crop width
            new_h = target_h
            new_w = int(target_h * src_ratio)
        else:
            # Source is taller: fit width, crop height
            new_w = target_w
            new_h = int(target_w / src_ratio)

        img = img.resize((new_w, new_h), Image.LANCZOS)

        # Center crop to exact target
        left = (new_w - target_w) // 2
        top = (new_h - target_h) // 2
        img = img.crop((left, top, left + target_w, top + target_h))

    # Build output path
    out_dir = Path(output_dir) if output_dir else src.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    out_name = f"{src.stem}-{preset}.webp"
    out_path = out_dir / out_name

    # Save as WebP
    img.save(out_path, 'WEBP', quality=quality)

    src_size = src.stat().st_size
    out_size = out_path.stat().st_size
    reduction = (1 - out_size / src_size) * 100 if src_size > 0 else 0

    print(f"Saved: {out_path}")
    print(f"  Dimensions: {img.width}x{img.height}")
    print(f"  Size: {src_size:,} -> {out_size:,} bytes ({reduction:.0f}% reduction)")

    # Update sidecar if it exists
    sidecar_path = src.with_suffix('.meta.json')
    if sidecar_path.exists():
        with open(sidecar_path, 'r') as f:
            meta = json.load(f)
        meta['webp_path'] = str(out_path.name)
        meta['webp_dimensions'] = {"width": img.width, "height": img.height}
        meta['webp_preset'] = preset
        with open(sidecar_path, 'w') as f:
            json.dump(meta, f, indent=2)
        print(f"  Updated sidecar: {sidecar_path.name}")

    return out_path


def main():
    parser = argparse.ArgumentParser(
        description="Convert images to WebP with dimension presets",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Presets:
    thumbnail       1200x675  (16:9, Webflow blog)
    social-square   1080x1080
    social-portrait 1080x1350
    inline          max-width 800px, proportional
        """,
    )
    parser.add_argument("image", help="Path to the source image")
    parser.add_argument(
        "--use", required=True,
        choices=list(PRESETS.keys()),
        help="Dimension preset to apply"
    )
    parser.add_argument(
        "--quality", "-q",
        type=int, default=85,
        help="WebP quality 1-100 (default: 85)"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output directory (default: same as input)"
    )

    args = parser.parse_args()
    optimize_image(
        input_path=args.image,
        preset=args.use,
        quality=args.quality,
        output_dir=args.output,
    )


if __name__ == "__main__":
    main()
