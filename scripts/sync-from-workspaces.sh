#!/bin/bash
# Sync skills FROM your workspaces TO Content OS
# Run this when you've updated skills in a workspace and want to propagate changes

set -e

CONTENT_OS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SKILLS_DIR="$CONTENT_OS_DIR/skills"

# Source workspaces (customize these paths)
SKILL_STACK="$HOME/skill-stack-temp/.claude/skills"
OPENED_CLEAN="$HOME/OpenEd-Clean/.claude/skills"

echo "Syncing skills to Content OS..."
echo ""

# Writing skills (from skill-stack)
echo "Writing skills..."
rsync -av --delete "$SKILL_STACK/ghostwriter/" "$SKILLS_DIR/writing/ghostwriter/"
rsync -av --delete "$SKILL_STACK/anti-ai-writing/" "$SKILLS_DIR/writing/anti-ai-writing/"
rsync -av --delete "$SKILL_STACK/writing-style/" "$SKILLS_DIR/writing/writing-style/"
rsync -av --delete "$SKILL_STACK/transcript-polisher/" "$SKILLS_DIR/writing/transcript-polisher/"
rsync -av --delete "$SKILL_STACK/hook-and-headline-writing/" "$SKILLS_DIR/writing/hook-and-headline-writing/"
rsync -av --delete "$SKILL_STACK/cold-open-creator/" "$SKILLS_DIR/writing/cold-open-creator/"
rsync -av --delete "$SKILL_STACK/dude-with-sign-writer/" "$SKILLS_DIR/writing/dude-with-sign-writer/"
rsync -av --delete "$SKILL_STACK/voice-pirate-wires/" "$SKILLS_DIR/writing/voice-pirate-wires/"

# Video skills (from skill-stack)
echo "Video skills..."
rsync -av --delete "$SKILL_STACK/youtube-clip-extractor/" "$SKILLS_DIR/video/youtube-clip-extractor/"
rsync -av --delete "$SKILL_STACK/youtube-downloader/" "$SKILLS_DIR/video/youtube-downloader/"
rsync -av --delete "$SKILL_STACK/youtube-title-creator/" "$SKILLS_DIR/video/youtube-title-creator/"
rsync -av --delete "$SKILL_STACK/video-caption-creation/" "$SKILLS_DIR/video/video-caption-creation/"
rsync -av --delete "$SKILL_STACK/podcast-production/" "$SKILLS_DIR/video/podcast-production/"
rsync -av --delete "$SKILL_STACK/podcast-blog-post-creator/" "$SKILLS_DIR/video/podcast-blog-post-creator/"

# Newsletter skills (mixed sources)
echo "Newsletter skills..."
rsync -av --delete "$SKILL_STACK/skill-stack-newsletter-writer/" "$SKILLS_DIR/newsletter/skill-stack-newsletter-writer/"
rsync -av --delete "$OPENED_CLEAN/opened-daily-newsletter-writer/" "$SKILLS_DIR/newsletter/opened-daily-newsletter-writer/"
rsync -av --delete "$OPENED_CLEAN/opened-weekly-newsletter-writer/" "$SKILLS_DIR/newsletter/opened-weekly-newsletter-writer/"

# Social skills (mixed sources)
echo "Social skills..."
rsync -av --delete "$SKILL_STACK/social-content-creation/" "$SKILLS_DIR/social/social-content-creation/"
rsync -av --delete "$OPENED_CLEAN/x-article-converter/" "$SKILLS_DIR/social/x-article-converter/"
rsync -av --delete "$OPENED_CLEAN/text-content/" "$SKILLS_DIR/social/text-content/"

# Brand-voice skills (mixed sources)
echo "Brand-voice skills..."
rsync -av --delete "$SKILL_STACK/brand-identity-wizard/" "$SKILLS_DIR/brand-voice/brand-identity-wizard/"
rsync -av --delete "$SKILL_STACK/voice-matching-wizard/" "$SKILLS_DIR/brand-voice/voice-matching-wizard/"
rsync -av --delete "$SKILL_STACK/voice-analyzer/" "$SKILLS_DIR/brand-voice/voice-analyzer/"
rsync -av --delete "$OPENED_CLEAN/opened-identity/" "$SKILLS_DIR/brand-voice/opened-identity/"
rsync -av --delete "$OPENED_CLEAN/guidelines-brand/" "$SKILLS_DIR/brand-voice/guidelines-brand/"

# Research skills (from OpenEd)
echo "Research skills..."
rsync -av --delete "$OPENED_CLEAN/seo-research/" "$SKILLS_DIR/research/seo-research/"
rsync -av --delete "$OPENED_CLEAN/seo-content-writer/" "$SKILLS_DIR/research/seo-content-writer/"

# Meta skills (from skill-stack)
echo "Meta skills..."
rsync -av --delete "$SKILL_STACK/skill-creator/" "$SKILLS_DIR/meta/skill-creator/"
rsync -av --delete "$SKILL_STACK/image-prompt-generator/" "$SKILLS_DIR/meta/image-prompt-generator/"

echo ""
echo "Sync complete!"
echo "Remember to commit changes to Content OS repo."
