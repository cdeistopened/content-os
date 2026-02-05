# Notion Integration

Connect to Notion workspaces for knowledge capture, meeting prep, and research documentation.

## Setup

1. Create an integration at [notion.so/my-integrations](https://www.notion.so/my-integrations)
2. Give it access to the pages/databases you want to use
3. Set environment variable:
   ```bash
   export NOTION_TOKEN=your-integration-token
   ```

## Used By

- **notion-knowledge-capture** — Save conversation insights to Notion
- **notion-meeting-intelligence** — Pull context from Notion for meeting prep
- **notion-research-documentation** — Store research findings
- **notion-spec-to-implementation** — Convert specs to task lists

## MCP Server

For Claude Code integration, configure the Notion MCP server in your `.claude/settings.json`:

```json
{
  "mcpServers": {
    "notion": {
      "command": "npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "your-token"
      }
    }
  }
}
```
