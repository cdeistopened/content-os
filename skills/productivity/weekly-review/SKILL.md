# Weekly Review Skill

Scan all project files across the workspace and generate an action-oriented status report with next steps.

---

## Purpose

1. **Status overview** — What's the state of each active project?
2. **Project completion focus** — What's closest to done? What's blocked?
3. **Action-oriented** — Concrete next steps, not vague summaries
4. **Proactive suggestions** — Surface what needs attention

---

## File Types to Scan

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Project context, goals, constraints |
| `NOW.md` | Current state, this week's priorities |
| `PROJECT.md` | Project spec, milestones, success criteria |

**Root CLAUDE.md** provides the map of what projects exist and their relationships.

---

## Scan Command

```bash
find "/Users/charliedeist/Desktop/New Root Docs" \
  \( -name "NOW.md" -o -name "PROJECT.md" -o -name "CLAUDE.md" \) \
  -type f 2>/dev/null | grep -v node_modules | grep -v ".git"
```

---

## Weekly Review Output Format

```markdown
# Weekly Review — [Date]

## 🎯 Focus Projects (Active This Week)

### [Project Name]
**Location:** `path/to/project`
**Status:** [One-line status from NOW.md]
**Progress:** [What moved since last week]
**Blockers:** [What's stuck]
**Next step:** [Single concrete action]

---

## 📦 Ready to Ship (Close to Done)

Projects that could be completed with focused effort:
1. **[Project]** — [What's left]

---

## ⏸️ On Hold / Dormant

Projects with no recent activity:
- [Project] — Last touched: [date]

---

## 🚨 Needs Attention

Projects with stale NOW.md or unclear next steps:
- [Project] — [Issue]

---

## Suggested Priorities This Week

Based on deadlines, momentum, and effort:

1. **[Project]** — [Why now]
2. **[Project]** — [Why now]
3. **[Project]** — [Why now]

---

## Quick Wins (< 30 min each)

- [ ] [Small task from Project X]
- [ ] [Small task from Project Y]
```

---

## How to Trigger

Say any of:
- `/review`
- "Run weekly review"
- "What's the status of my projects?"
- "Show me project status across workspace"

---

## Review Process

### Step 1: Discover Projects
Scan for CLAUDE.md, NOW.md, PROJECT.md files. Build project list.

### Step 2: Read Current State
For each project with NOW.md, extract:
- Current status
- This week's tasks
- What's done vs. pending

### Step 3: Identify Patterns
- Which projects have momentum?
- Which are stale (NOW.md > 7 days old)?
- Which have unclear next steps?

### Step 4: Generate Report
Output the weekly review format above.

### Step 5: Update Root NOW.md (Optional)
Offer to update the workspace NOW.md with this week's priorities.

---

## Known Project Locations

### Personal / Writing
- `Personal/Benedict Challenge/` — Book + Vigil app (Deadline: March 4)
- `Personal/JFK50/` — 50-mile march book
- `Personal/CLM Publishing/` — Catholic social teaching books

### Work
- `OpenEd Vault/Studio/Lead Magnet Project/` — Curriculove + guides
- `OpenEd Vault/Studio/Social Media/` — Content engine

### Creative Intelligence Agency
- `Creative Intelligence Agency/skill-stack/` — Skill Stack newsletter/site
- `Creative Intelligence Agency/wiki-projects/` — Various wiki projects
- `Creative Intelligence Agency/clients/` — Client work (Naval, Pause)

---

## Success Criteria

A good weekly review should:
- [ ] Take < 5 minutes to generate
- [ ] Surface the 3 most important things to do this week
- [ ] Identify at least one project that's close to shipping
- [ ] Flag any project that's been neglected

---

*Philosophy: Review is for clarity, not guilt. The goal is to see the whole map, pick the right trail, and take one step.*
