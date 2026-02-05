# Slack CLI & MCP

Access Slack via MCP tools (preferred) or clawdbot's slack tool.

---

## MCP Tools (Preferred in Claude Code)

These work directly in Claude Code sessions:

```
mcp__slack__channels_list
mcp__slack__conversations_history
mcp__slack__conversations_replies
mcp__slack__conversations_search_messages
mcp__slack__conversations_add_message
```

### Search Messages

```
mcp__slack__conversations_search_messages
  - search_query: "keyword"
  - filter_in_channel: "#general" or "C1234567890"
  - filter_users_from: "@username" or "U1234567890"
  - filter_date_after: "2026-01-01"
  - limit: 20
```

### Get Channel History

```
mcp__slack__conversations_history
  - channel_id: "C1234567890" or "#general"
  - limit: "7d" or "50"
```

### Send Message

```
mcp__slack__conversations_add_message
  - channel_id: "#general" or "C1234567890"
  - payload: "Your message here"
  - thread_ts: "1234567890.123456" (optional, for thread replies)
```

---

## OpenEd Team Reference

| Person | User ID | DM Channel |
|--------|---------|------------|
| Ela Bass | U071HDEDU1J | D071JERTN3H |
| Chavilah Stowers | U08MXSP81EJ | D08N19QFRPH |
| Isaac Morehouse | U06T2T5H7DE | D072DJRDKS5 |
| Jared Fuller | U07HNPG7E2Y | D07HNPG7E2Y |
| Melissa Wurzel | U08JGDE6YLW | - |
| Grant Hewitt | U07KSTJKFV1 | - |
| Andrea Fife | U01FQ7E0EJY | D071UD7HSHK |
| Alex Hernandez | U07276F8L1W | D07287S2K16 |

## Key Channels

| Channel | ID |
|---------|-----|
| #market-daily | C07U9S53TLL |
| #market-working | C072LQLAFGA |
| #team-market | C08FEV1SZGP |

---

## Via Clawdbot (JSON Actions)

When using clawdbot's slack tool:

```json
{"action": "react", "channelId": "C123", "messageId": "1712023032.1234", "emoji": "✅"}
{"action": "sendMessage", "to": "channel:C123", "content": "Hello"}
{"action": "pinMessage", "channelId": "C123", "messageId": "1712023032.1234"}
{"action": "memberInfo", "userId": "U123"}
```

---

## Tips

- Use MCP tools for direct API access in Claude Code
- Message IDs are timestamps like `1712023032.1234`
- Always confirm before sending messages on behalf of user
