---
name: draft_reply
description: Use Gmail MCP to draft replies for incoming emails in the vault
---

# Draft Reply Skill 📬

## Purpose
Helps you respond to emails by drafting professional replies directly in your Gmail account.

## When to Use
- You see a new email in `/Needs_Action`.
- You want the AI to suggest a professional response.
- You want to see the draft in your "Drafts" folder before clicking Send.

## Workflow

### 1. Identify Target Email
Read the email metadata from the file in `/Needs_Action` (look for Subject and Thread ID).

### 2. Craft Professional Response
Use the `Company_Handbook.md` rules (professional but friendly) to write the response content.

### 3. Create Draft in Gmail
Use the `gmail.create_draft` tool from the MCP server to save the reply.

### 4. Notify User
Confirm the draft is ready and provide a link to your Gmail Drafts folder.

## Tools Required
- **filesystem**: To read `/Needs_Action` and `Company_Handbook.md`
- **gmail**: `gmail.create_draft` (from MCP)

## Rules of Engagement
- ❌ **NEVER** use `gmail.send_message` directly.
- ✅ **ALWAYS** use `gmail.create_draft` first.
- ✅ Wait for human approval before moving the action file to `/Done`.
