---
name: silver_safety
description: Teaches the AI to wait for human approval before taking any external action.
---

# Silver Tier Safety Skill (HITL)

## Purpose
Ensures that the AI does not send emails, post to social media, or make payments without explicit human permission.

## When to Use This Skill
- Before sending an email using an MCP tool.
- Before posting content to LinkedIn/WhatsApp.
- For any action defined as "Sensitive" in the `Company_Handbook.md`.

## Workflow

### Step 1: Detect Sensitive Action Needed
When the AI (Claude Code) decides that an external action is required (e.g., replying to a client or posting a summary).

### Step 2: Create Approval Request
DO NOT execute the action tool yet. Instead, create a file in `/Pending_Approval/`:

```markdown
---
type: approval_request
action: [e.g., send_email, post_linkedin]
recipient: [e.g., client@example.com]
subject: [e.g., Invoice #1234]
created: {{timestamp}}
status: pending
---

# 🛡️ Approval Request: [Action Title]

## Action Details
- **Type**: [e.g. Email / LinkedIn Post]
- **Target**: [Recipient / Platform]
- **Content**:
> [Insert the exact text of the email or post here]

## 🛠️ To Approve
Move this file to `/Approved` folder.

## ❌ To Reject
Move this file to `/Rejected` folder.
```

### Step 3: Inform User
Report back to the user: "Drafted the [action] and saved it in /Pending_Approval. I will execute once you move the file to the /Approved folder."

## Next Steps (Orchestrator)
The `orchestrator.py` will monitor the `/Approved` folder and trigger the actual action tool once the file appears there.

## Success Criteria
✅ Sensitive content is never sent automatically.
✅ All drafted actions are stored in `/Pending_Approval`.
✅ The system waits for human "Eyes on Target".
