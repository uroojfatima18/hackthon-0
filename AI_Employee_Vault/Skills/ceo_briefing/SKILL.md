# 📊 CEO Briefing Skill

This skill allows the AI Agent to perform a weekly business audit and generate a "Monday Morning CEO Briefing".

## Objectives
- Read `Business_Goals.md` to understand targets.
- Analyze recent task completions in `/Done`.
- Summarize financial data (from `audit_logic.py` output or bank files).
- Identify bottlenecks and provide proactive suggestions.

## Workflow
1. Read the core business goals from the root of the vault.
2. Scan the `/Logs` and `/Done` folders to see what happened in the last 7 days.
3. Use the `audit_logic.py` (if applicable) to see subscription alerts or revenue.
4. Compose a markdown file in `/Pending_Approval` named `APPROVAL_REQUIRED_Briefing_YYYY-MM-DD.md`.
5. The briefing MUST follow the format:
    - **Executive Summary**
    - **Revenue vs Target**
    - **Completed Tasks (Highlights)**
    - **Bottlenecks (Delays)**
    - **Proactive Suggestions** (e.g., "Cancel unused subscription", "Follow up with Client X")

## Rules
- NEVER approve your own briefing.
- Flag any expense over $100 for manual review.
- If revenue is behind target, suggest at least one sales-focused task.
