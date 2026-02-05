# remindctl - Apple Reminders CLI

Manage Apple Reminders from the terminal.

---

## Available Lists

Inbox, Benedict, CLM, Doodle Docs, Errands, Family, Farm, Life OS, MBHP, Meeting With Emma, Naval, OpenEd, Ray Peat, Shopping, Skill Stack

---

## Priority System (1-3-9)

| Flag | Priority | Meaning |
|------|----------|---------|
| `--priority high` | #1 | Big Rock / Deep Work |
| `--priority medium` | #3 | Pomodoro (~25-50 min) |
| `--priority low` | #9 | Quick task (~5-15 min) |

---

## View Reminders

```bash
remindctl                    # Today's reminders
remindctl today              # Today
remindctl tomorrow           # Tomorrow
remindctl week               # This week
remindctl overdue            # Overdue items
remindctl upcoming           # Upcoming
remindctl completed          # Completed
remindctl all                # Everything
remindctl 2026-01-20         # Specific date
```

---

## Manage Lists

```bash
remindctl list                      # Show all lists with counts
remindctl list "Inbox"              # Show reminders in Inbox
remindctl list "Inbox" --json       # JSON output
remindctl list "Projects" --create  # Create new list
remindctl list "Old" --delete       # Delete list
```

---

## Create Reminders

```bash
# Quick add to default list
remindctl add "Buy milk"

# Add to specific list with due date
remindctl add --title "Call mom" --list Personal --due tomorrow

# Add with priority
remindctl add --title "Deep work on manuscript" --list Benedict --due today --priority high

# Add with notes
remindctl add --title "Review PR" --list OpenEd --priority medium --notes "Check the auth changes"
```

---

## Edit & Complete

```bash
# Edit reminder
remindctl edit 1 --title "New title" --due 2026-01-25

# Complete reminders by ID
remindctl complete 1 2 3

# Delete reminder
remindctl delete 4A83 --force
```

---

## Output Formats

```bash
remindctl today --json    # JSON (for scripting)
remindctl today --plain   # Plain TSV
remindctl today --quiet   # Counts only
```

---

## Date Formats

Accepted by `--due`:
- `today`, `tomorrow`, `yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601 (`2026-01-20T12:00:00Z`)

---

## Notes

- macOS only
- Grant Reminders permission in System Settings → Privacy & Security → Reminders
- IDs are shown in brackets: `[1]`, `[2]`, etc.
