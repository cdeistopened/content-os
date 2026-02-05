# gog - Google Workspace CLI

Gmail, Calendar, Drive, Contacts, Sheets, and Docs from the terminal.

---

## Configured Accounts

| Account | Services | Use |
|---------|----------|-----|
| `chdeist@gmail.com` | gmail, calendar, contacts, drive | Personal |
| `cdeist@opened.co` | gmail, calendar, contacts, drive | Work (OpenEd) |

**Always specify account:** `--account chdeist@gmail.com` or set `GOG_ACCOUNT` env var.

---

## Gmail

```bash
# Search
gog gmail search "is:unread" --account chdeist@gmail.com --max 10
gog gmail search "from:someone newer_than:7d" --account cdeist@opened.co

# Read message
gog gmail read <messageId> --account chdeist@gmail.com

# Send (plain text)
gog gmail send --to recipient@example.com --subject "Subject" --body "Message" --account chdeist@gmail.com

# Send (multi-line via stdin)
gog gmail send --to recipient@example.com --subject "Subject" --body-file - --account chdeist@gmail.com <<'EOF'
Hi there,

This is a multi-paragraph email.

Best,
Charlie
EOF

# Create draft
gog gmail drafts create --to a@b.com --subject "Hi" --body "Draft content" --account chdeist@gmail.com

# Send draft
gog gmail drafts send <draftId> --account chdeist@gmail.com

# Reply to thread
gog gmail send --to a@b.com --subject "Re: Original" --body "Reply" --reply-to-message-id <msgId> --account chdeist@gmail.com
```

---

## Calendar

```bash
# List events
gog calendar events primary --from 2026-01-19 --to 2026-01-26 --account chdeist@gmail.com

# Create event
gog calendar create primary --summary "Meeting" --from "2026-01-20T10:00:00" --to "2026-01-20T11:00:00" --account chdeist@gmail.com

# Create with color (1-11)
gog calendar create primary --summary "Important" --from <iso> --to <iso> --event-color 11 --account chdeist@gmail.com

# Show available colors
gog calendar colors
```

**Event Colors:** 1=#a4bdfc, 2=#7ae7bf, 3=#dbadff, 4=#ff887c, 5=#fbd75b, 6=#ffb878, 7=#46d6db, 8=#e1e1e1, 9=#5484ed, 10=#51b749, 11=#dc2127

---

## Drive

```bash
# Search files
gog drive search "name contains 'report'" --account chdeist@gmail.com --max 10

# List files
gog drive list --account chdeist@gmail.com --max 20
```

---

## Contacts

```bash
gog contacts list --account chdeist@gmail.com --max 20
gog contacts search "John" --account chdeist@gmail.com
```

---

## Sheets

```bash
# Read range
gog sheets get <sheetId> "Sheet1!A1:D10" --json --account chdeist@gmail.com

# Update cells
gog sheets update <sheetId> "Sheet1!A1:B2" --values-json '[["A","B"],["1","2"]]' --input USER_ENTERED --account chdeist@gmail.com

# Append rows
gog sheets append <sheetId> "Sheet1!A:C" --values-json '[["x","y","z"]]' --insert INSERT_ROWS --account chdeist@gmail.com

# Clear range
gog sheets clear <sheetId> "Sheet1!A2:Z" --account chdeist@gmail.com

# Get metadata
gog sheets metadata <sheetId> --json --account chdeist@gmail.com
```

---

## Docs

```bash
# Export to text
gog docs export <docId> --format txt --out /tmp/doc.txt --account chdeist@gmail.com

# Cat contents
gog docs cat <docId> --account chdeist@gmail.com
```

---

## Tips

- Use `--json` for scripting output
- Use `--no-input` to skip confirmations in scripts
- Confirm before sending mail or creating events
- For multi-line email bodies, use `--body-file -` with heredoc
