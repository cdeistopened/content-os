#!/usr/bin/env python3
"""
Gemini Context Delegation - Delegate context-heavy tasks to Gemini 3 Flash.

Leverages Gemini's 1M token context window for tasks requiring massive
amounts of reading, analysis, or synthesis.

Modes:
- analyze: Read sources, return analysis (no file writing)
- transform: Read sources, write transformed outputs
- agent: Autonomous operation with tool access (for complex tasks)
"""

import os
import sys
import json
import argparse
import glob as globlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Any, Optional

from dotenv import load_dotenv

load_dotenv()

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("Error: google-genai not installed.")
    print("Run: pip install google-genai python-dotenv")
    sys.exit(1)


MODEL_NAME = "gemini-3-flash-preview"  # CRITICAL: Do not change this model name
TOKEN_LIMIT = 1_000_000
COMPRESSION_THRESHOLD = 900_000
MAX_ITERATIONS_AGENT_MODE = 300
BACKUP_INTERVAL = 50


def load_sources(
    source_path: str, extensions: Optional[List[str]] = None
) -> Dict[str, str]:
    """
    Load all source files from a path.

    Args:
        source_path: File or directory path
        extensions: Optional list of extensions to filter (e.g., ['.md', '.txt'])

    Returns:
        Dict mapping filename to content
    """
    sources = {}
    path = Path(source_path)

    if path.is_file():
        try:
            content = path.read_text(encoding="utf-8")
            sources[path.name] = content
        except Exception as e:
            print(f"Warning: Could not read {path}: {e}")

    elif path.is_dir():
        if extensions is None:
            extensions = [
                ".md",
                ".txt",
                ".py",
                ".js",
                ".ts",
                ".jsx",
                ".tsx",
                ".json",
                ".yaml",
                ".yml",
                ".html",
                ".css",
                ".sql",
                ".sh",
                ".bash",
                ".go",
                ".rs",
                ".java",
                ".rb",
                ".php",
            ]

        for ext in extensions:
            for file_path in path.rglob(f"*{ext}"):
                if file_path.is_file():
                    try:
                        rel_path = file_path.relative_to(path)
                        content = file_path.read_text(encoding="utf-8")
                        sources[str(rel_path)] = content
                    except Exception as e:
                        print(f"Warning: Could not read {file_path}: {e}")

    return sources


def estimate_tokens(text: str) -> int:
    """Rough token estimate: ~4 characters per token."""
    return len(text) // 4


def format_sources_for_context(sources: Dict[str, str]) -> str:
    """Format sources into a single context string."""
    parts = []
    for filename, content in sources.items():
        parts.append(f"=== FILE: {filename} ===\n{content}\n")
    return "\n".join(parts)


def run_analyze_mode(
    client: genai.Client, sources: Dict[str, str], prompt: str, max_tokens: int
) -> str:
    """
    Analyze mode: Read sources and return analysis.

    Returns the analysis as a string.
    """
    context = format_sources_for_context(sources)

    full_prompt = f"""You have access to the following source files:

{context}

=== TASK ===
{prompt}

Provide your analysis based on the sources above."""

    token_estimate = estimate_tokens(full_prompt)
    print(f"Input tokens (estimated): {token_estimate:,}")

    if token_estimate > TOKEN_LIMIT:
        print(
            f"Warning: Input exceeds token limit ({token_estimate:,} > {TOKEN_LIMIT:,})"
        )
        print("Consider splitting sources or using agent mode with compression.")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)])
        ],
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=max_tokens,
        ),
    )

    return response.text or ""


def run_transform_mode(
    client: genai.Client,
    sources: Dict[str, str],
    prompt: str,
    output_dir: str,
    max_tokens: int,
) -> Dict[str, Any]:
    """
    Transform mode: Read sources and write transformed outputs.

    Returns dict with results summary.
    """
    os.makedirs(output_dir, exist_ok=True)

    context = format_sources_for_context(sources)

    full_prompt = f"""You have access to the following source files:

{context}

=== TASK ===
{prompt}

=== OUTPUT FORMAT ===
For each output file you want to create, use this format:

<<<FILE: filename.ext>>>
[file content here]
<<<END FILE>>>

You can create multiple files. Include all content in the appropriate file sections."""

    token_estimate = estimate_tokens(full_prompt)
    print(f"Input tokens (estimated): {token_estimate:,}")

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[
            types.Content(role="user", parts=[types.Part.from_text(text=full_prompt)])
        ],
        config=types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=max_tokens,
        ),
    )

    output_text = response.text or ""

    files_created = []
    import re

    file_pattern = r"<<<FILE:\s*(.+?)>>>\n(.*?)<<<END FILE>>>"
    matches = re.findall(file_pattern, output_text, re.DOTALL)

    for filename, content in matches:
        filename = filename.strip()
        file_path = os.path.join(output_dir, filename)
        os.makedirs(
            os.path.dirname(file_path) if os.path.dirname(file_path) else output_dir,
            exist_ok=True,
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content.strip())

        files_created.append(filename)
        print(f"Created: {filename}")

    if not files_created:
        raw_path = os.path.join(output_dir, "output.md")
        with open(raw_path, "w", encoding="utf-8") as f:
            f.write(output_text)
        files_created.append("output.md")
        print("Created: output.md (raw output)")

    return {
        "files_created": files_created,
        "output_dir": output_dir,
    }


def get_agent_tools() -> types.Tool:
    """Get tool definitions for agent mode."""
    return types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="write_file",
                description="Write content to a file in the output directory.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "filename": types.Schema(
                            type=types.Type.STRING,
                            description="Filename (can include subdirectories)",
                        ),
                        "content": types.Schema(
                            type=types.Type.STRING, description="Content to write"
                        ),
                        "mode": types.Schema(
                            type=types.Type.STRING,
                            enum=["create", "append", "overwrite"],
                            description="Write mode",
                        ),
                    },
                    required=["filename", "content", "mode"],
                ),
            ),
            types.FunctionDeclaration(
                name="task_complete",
                description="Signal that the task is complete.",
                parameters=types.Schema(
                    type=types.Type.OBJECT,
                    properties={
                        "summary": types.Schema(
                            type=types.Type.STRING,
                            description="Brief summary of what was accomplished",
                        )
                    },
                    required=["summary"],
                ),
            ),
        ]
    )


def execute_tool(tool_name: str, args: Dict[str, Any], output_dir: str) -> str:
    """Execute a tool call and return result."""
    if tool_name == "write_file":
        filename = args.get("filename", "output.md")
        content = args.get("content", "")
        mode = args.get("mode", "create")

        file_path = os.path.join(output_dir, filename)
        os.makedirs(
            os.path.dirname(file_path) if os.path.dirname(file_path) else output_dir,
            exist_ok=True,
        )

        if mode == "create" and os.path.exists(file_path):
            return (
                f"Error: File '{filename}' already exists. Use 'append' or 'overwrite'."
            )

        write_mode = "a" if mode == "append" else "w"
        with open(file_path, write_mode, encoding="utf-8") as f:
            f.write(content)

        return f"Successfully wrote {len(content)} chars to '{filename}' (mode: {mode})"

    elif tool_name == "task_complete":
        return "TASK_COMPLETE"

    return f"Unknown tool: {tool_name}"


def run_agent_mode(
    client: genai.Client,
    sources: Dict[str, str],
    prompt: str,
    output_dir: str,
    recovery_context: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Agent mode: Autonomous operation with tool access.

    Runs iteratively, allowing Gemini to call tools until task completion.
    """
    os.makedirs(output_dir, exist_ok=True)

    if recovery_context:
        initial_message = f"[RECOVERED CONTEXT]\n\n{recovery_context}\n\n[END CONTEXT]\n\nContinue from where we left off."
    else:
        context = format_sources_for_context(sources)
        initial_message = f"""You have access to the following source files:

{context}

=== TASK ===
{prompt}

=== INSTRUCTIONS ===
Work through this task step by step. Use the write_file tool to create output files.
When finished, call task_complete with a summary.

Write SUBSTANTIAL content - don't abbreviate or summarize when full content is needed."""

    contents: List[types.Content] = [
        types.Content(role="user", parts=[types.Part.from_text(text=initial_message)])
    ]

    tools = get_agent_tools()
    system_instruction = """You are an expert analyst and writer. Your task is to process 
the provided sources and complete the requested task thoroughly.

Guidelines:
- Write complete, substantial content
- Use write_file to save your work incrementally
- Call task_complete when finished
- Be thorough - don't abbreviate"""

    files_created = []

    for iteration in range(1, MAX_ITERATIONS_AGENT_MODE + 1):
        print(f"\n--- Iteration {iteration}/{MAX_ITERATIONS_AGENT_MODE} ---")

        token_estimate = sum(estimate_tokens(str(c)) for c in contents)
        print(f"Context tokens (est): {token_estimate:,}")

        if token_estimate > COMPRESSION_THRESHOLD:
            print("Warning: Approaching token limit. Consider compression.")

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=[tools],
                    temperature=0.7,
                ),
            )
        except Exception as e:
            print(f"API Error: {e}")
            continue

        model_content = response.candidates[0].content if response.candidates else None
        if not model_content:
            print("No response from model")
            continue

        contents.append(model_content)

        function_calls = []
        for part in model_content.parts:
            if hasattr(part, "function_call") and part.function_call:
                function_calls.append(
                    {
                        "name": part.function_call.name,
                        "args": dict(part.function_call.args)
                        if part.function_call.args
                        else {},
                    }
                )
            elif hasattr(part, "text") and part.text:
                print(
                    f"Response: {part.text[:200]}..."
                    if len(part.text) > 200
                    else f"Response: {part.text}"
                )

        if not function_calls:
            print("No tool calls - task may be complete")
            break

        function_response_parts = []
        task_complete = False

        for fc in function_calls:
            print(f"Tool: {fc['name']}")
            result = execute_tool(fc["name"], fc["args"], output_dir)

            if result == "TASK_COMPLETE":
                task_complete = True
                summary = fc["args"].get("summary", "Task completed")
                print(f"\n=== TASK COMPLETE ===\n{summary}")
                result = "Task marked complete."

            if fc["name"] == "write_file" and "Successfully" in result:
                files_created.append(fc["args"].get("filename", "unknown"))

            function_response_parts.append(
                types.Part.from_function_response(
                    name=fc["name"], response={"result": result}
                )
            )

        contents.append(types.Content(role="user", parts=function_response_parts))

        if task_complete:
            break

        if iteration % BACKUP_INTERVAL == 0:
            backup_path = os.path.join(
                output_dir,
                f".context_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
            )
            try:
                with open(backup_path, "w", encoding="utf-8") as f:
                    f.write(f"# Context Backup - Iteration {iteration}\n\n")
                    for c in contents[-10:]:
                        role = c.role
                        for p in c.parts:
                            if hasattr(p, "text") and p.text:
                                f.write(f"## {role}\n{p.text}\n\n")
                print(f"Backup saved: {backup_path}")
            except Exception as e:
                print(f"Backup failed: {e}")

    return {
        "files_created": files_created,
        "iterations": iteration,
        "output_dir": output_dir,
    }


def main():
    parser = argparse.ArgumentParser(
        description="Delegate context-heavy tasks to Gemini 3 Flash",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "--sources", "-s", required=True, help="Path to source file or directory"
    )
    parser.add_argument(
        "--output",
        "-o",
        default="./output",
        help="Output directory (default: ./output)",
    )
    parser.add_argument(
        "--prompt", "-p", required=True, help="Task description for Gemini"
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["analyze", "transform", "agent"],
        default="analyze",
        help="Operation mode (default: analyze)",
    )
    parser.add_argument(
        "--recover", "-r", help="Path to context summary for recovery (agent mode)"
    )
    parser.add_argument(
        "--max-tokens", type=int, default=8192, help="Max output tokens (default: 8192)"
    )
    parser.add_argument(
        "--extensions", nargs="+", help="File extensions to include (e.g., .py .md)"
    )

    args = parser.parse_args()

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY not set")
        print("Set via: export GEMINI_API_KEY='your-key'")
        sys.exit(1)

    print(f"API Key: {api_key[:4]}...{api_key[-4:]}")

    client = genai.Client(api_key=api_key)
    print(f"Model: {MODEL_NAME}")
    print(f"Mode: {args.mode}")

    if args.recover and args.mode == "agent":
        sources = {}
        recovery_context = Path(args.recover).read_text(encoding="utf-8")
        print(f"Recovery context loaded: {len(recovery_context)} chars")
    else:
        extensions = (
            [f".{e.lstrip('.')}" for e in args.extensions] if args.extensions else None
        )
        sources = load_sources(args.sources, extensions)
        recovery_context = None

        if not sources:
            print(f"Error: No sources found at {args.sources}")
            sys.exit(1)

        print(f"Loaded {len(sources)} source file(s)")
        total_chars = sum(len(c) for c in sources.values())
        print(f"Total chars: {total_chars:,} (~{total_chars // 4:,} tokens)")

    print("\n" + "=" * 60)

    if args.mode == "analyze":
        result = run_analyze_mode(client, sources, args.prompt, args.max_tokens)
        print("\n=== ANALYSIS RESULT ===\n")
        print(result)

    elif args.mode == "transform":
        result = run_transform_mode(
            client, sources, args.prompt, args.output, args.max_tokens
        )
        print(f"\n=== TRANSFORM COMPLETE ===")
        print(f"Files created: {len(result['files_created'])}")
        for f in result["files_created"]:
            print(f"  - {f}")

    elif args.mode == "agent":
        result = run_agent_mode(
            client, sources, args.prompt, args.output, recovery_context
        )
        print(f"\n=== AGENT COMPLETE ===")
        print(f"Iterations: {result['iterations']}")
        print(f"Files created: {len(result['files_created'])}")
        for f in result["files_created"]:
            print(f"  - {f}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
