---
source: /Needs_Action/ACTION_APIs.md
priority: 🔴 URGENT
created: 2026-02-27T00:40:00Z
status: pending
---

# Action Plan: APIs.txt

## ⚠️ Security Alert
This file contains multiple **Active API Keys** for several services. Storing these in plain text in the vault is a security risk.

## Summary
The file contains credentials for:
- GitHub (Personal Access Token)
- Gemini (Multiple keys)
- Claude (Paid API key)
- OpenAI (Project key)
- Neon Database (PostgreSQL URL)
- Qdrant (API key and cluster endpoint)

## Recommended Actions
1. [ ] **Secure Credentials**: Move all keys to a `.env` file in the project root.
2. [ ] **Update Configs**: Update the orchestrator or any scripts to use environment variables instead of hardcoded keys.
3. [ ] **Sanitize vault**: Delete `Inbox/APIs.txt` and `Needs_Action/ACTION_APIs.md` once secured.
4. [ ] **Rotate Keys**: (Optional but Recommended) If this vault is ever pushed to a public repo, all these keys must be revoked and rotated.

## Timeline
- **Deadline**: ASAP
- **Suggested completion**: Within 10 minutes.

## Next Steps
I will wait for you to move the keys to a secure location before I "archive" this file.
