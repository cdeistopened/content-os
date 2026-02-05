# bird - Twitter/X CLI

Read, search, and post to X/Twitter from the terminal.

---

## Auth Status

**Not configured yet.** To set up:

1. Log into x.com in Safari or Chrome
2. Run `bird check` to verify cookies detected
3. Or set env vars: `AUTH_TOKEN` and `CT0`

---

## Read & Search

```bash
# Check auth
bird whoami

# Read a tweet
bird read <url-or-id>

# Read full thread
bird thread <url-or-id>

# Search
bird search "Naval Ravikant" -n 10
bird search "from:naval" -n 5
bird search "#buildinpublic" -n 20
```

---

## Post (Confirm First!)

```bash
# Post a tweet
bird tweet "Your tweet text here"

# Reply to a tweet
bird reply <id-or-url> "Your reply text"
```

**Always confirm with user before posting.**

---

## Auth Sources

1. **Browser cookies** (default) - Firefox, Chrome, or Safari
2. **Sweetistics API** - Set `SWEETISTICS_API_KEY` or use `--engine sweetistics`
3. **Manual** - `--auth-token` and `--ct0` flags

Check status: `bird check`

---

## Tips

- Use thread URLs to read full conversations
- Search operators: `from:user`, `to:user`, `#hashtag`, `since:2026-01-01`
- For posting, draft in a file first, review, then post
