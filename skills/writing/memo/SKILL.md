# memo - Apple Notes CLI

Manage Apple Notes from the terminal.

---

## View Notes

```bash
# List all notes
memo notes

# Filter by folder
memo notes -f "Folder Name"

# Search notes (fuzzy)
memo notes -s "search query"
```

---

## Create Notes

```bash
# Interactive create
memo notes -a

# Quick create with title
memo notes -a "Note Title"
```

---

## Edit & Delete

```bash
# Edit (interactive selection)
memo notes -e

# Delete (interactive selection)
memo notes -d
```

---

## Move & Export

```bash
# Move note to folder (interactive)
memo notes -m

# Export to HTML/Markdown (interactive)
memo notes -ex
```

---

## Limitations

- Cannot edit notes containing images/attachments
- Interactive prompts require terminal access
- macOS only

---

## Setup

If permission issues:
1. System Settings → Privacy & Security → Automation
2. Enable Terminal access to Notes.app
