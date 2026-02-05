"""Gemini audio transcription module."""

import os
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Optional
from urllib.request import urlopen, Request

from google import genai
from google.genai import types


@dataclass
class TranscriptionResult:
    """Result of a transcription."""
    text: str
    input_tokens: int
    output_tokens: int
    input_cost: float
    output_cost: float

    @property
    def total_cost(self) -> float:
        return self.input_cost + self.output_cost


class GeminiTranscriber:
    """Transcribe audio using Gemini 3 Flash Preview."""

    # Pricing: Gemini 3 Flash Preview
    INPUT_COST_PER_MILLION = 1.00  # Audio
    OUTPUT_COST_PER_MILLION = 3.00

    def __init__(self, api_key: Optional[str] = None, thinking_budget: int = 8192):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not set")

        self.client = genai.Client(api_key=self.api_key)
        self.thinking_budget = thinking_budget

    def download_audio(self, url: str, max_size_mb: int = 200) -> Optional[bytes]:
        """Download audio file from URL."""
        try:
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urlopen(req, timeout=120) as response:
                content_length = response.headers.get('Content-Length')
                if content_length and int(content_length) > max_size_mb * 1024 * 1024:
                    return None
                return response.read()
        except Exception:
            return None

    def transcribe(
        self,
        audio_data: bytes,
        prompt: str,
        mime_type: str = "audio/mpeg"
    ) -> TranscriptionResult:
        """
        Transcribe audio data using Gemini.

        Args:
            audio_data: Raw audio bytes
            prompt: The transcription prompt with context
            mime_type: Audio MIME type (default: audio/mpeg)

        Returns:
            TranscriptionResult with text and token usage
        """
        # Save audio to temp file for upload
        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as f:
            f.write(audio_data)
            temp_path = f.name

        try:
            # Upload file to Gemini
            uploaded_file = self.client.files.upload(file=temp_path)

            # Transcribe
            response = self.client.models.generate_content(
                model="gemini-3-flash-preview",
                contents=[
                    types.Content(
                        role="user",
                        parts=[
                            types.Part.from_uri(
                                file_uri=uploaded_file.uri,
                                mime_type=mime_type
                            ),
                            types.Part.from_text(text=prompt),
                        ],
                    ),
                ],
                config=types.GenerateContentConfig(
                    max_output_tokens=65536,
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(
                        thinking_budget=self.thinking_budget,
                    ),
                ),
            )

            # Extract token counts
            input_tokens = 0
            output_tokens = 0
            if response.usage_metadata:
                input_tokens = getattr(response.usage_metadata, 'prompt_token_count', 0) or 0
                output_tokens = getattr(response.usage_metadata, 'candidates_token_count', 0) or 0

            # Clean up uploaded file
            try:
                self.client.files.delete(name=uploaded_file.name)
            except:
                pass

            # Calculate costs
            input_cost = (input_tokens / 1_000_000) * self.INPUT_COST_PER_MILLION
            output_cost = (output_tokens / 1_000_000) * self.OUTPUT_COST_PER_MILLION

            return TranscriptionResult(
                text=response.text,
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                input_cost=input_cost,
                output_cost=output_cost,
            )

        finally:
            # Clean up temp file
            os.unlink(temp_path)

    def transcribe_from_url(
        self,
        audio_url: str,
        prompt: str,
        max_size_mb: int = 200
    ) -> Optional[TranscriptionResult]:
        """Download audio from URL and transcribe."""
        audio_data = self.download_audio(audio_url, max_size_mb)
        if not audio_data:
            return None
        return self.transcribe(audio_data, prompt)


def build_prompt(
    template: str,
    podcast_name: str,
    title: str,
    description: str = "",
    context: str = "",
    host_hints: str = "",
) -> str:
    """Build transcription prompt from template."""
    return template.format(
        podcast_name=podcast_name,
        title=title,
        description=f"Description: {description}" if description else "",
        context=context,
        host_hints=host_hints,
    )
