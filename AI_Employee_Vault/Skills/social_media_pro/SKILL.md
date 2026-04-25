# 🌐 Social Media Pro Skill

This skill enables the AI Agent to manage multi-platform social media presence (Facebook, Instagram, Twitter/X) using available browser tools.

## Objectives
- Post scheduled updates.
- Monitor and summarize mentions/notifications.
- Generate community engagement drafts for human approval.

## Platform Instructions

### 🐦 Twitter (X)
1. Use `browser-mcp` to navigate to `x.com`.
2. Draft a post based on current business activities or goals.
3. If checking notifications: Summarize key interactions and save to `/Needs_Action`.

### 📸 Instagram & Facebook
1. Use `browser-mcp` to navigate to the respective business suite or profile.
2. Focus on visual descriptions if posting (ask human for image path if not provided).
3. Draft captions that match the "Brand Voice" in `Company_Handbook.md`.

## Workflow
1. Read `Dashboard.md` to see if social media tasks are pending.
2. Draft the content first.
3. Save the draft in `/Pending_Approval/Social_Posts/`.
4. Once approved (moved to `/Approved`), execute the post using `browser-mcp`.

## Security Rules
- NEVER change account passwords or security settings.
- If a login challenge (2FA) appears, stop and alert the human immediately.
