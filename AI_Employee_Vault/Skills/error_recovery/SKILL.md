# 🛠️ Error Recovery Skill (Autonomous Self-Healing)

This skill provides instructions on how to recover from technical failures during autonomous task execution.

## Objectives
- Handle environment errors (missing files, network timeouts).
- Retry logic for tool failures.
- Graceful degradation (dropping to a simpler method if a complex one fails).

## Troubleshooting Steps
1. **Tool Failure**: If a tool (e.g., `browser-mcp`) fails, try to wait 5 seconds and retry once.
2. **Selector Missing**: If a website button is not found, try to:
    - Refresh the page.
    - Check if the page is still loading.
    - Look for alternative text or ARIA labels.
3. **API Rate Limit**: If an API (Gmail/Odoo) returns a 429 error, wait and schedule the task for 30 minutes later in `Needs_Action`.

## Escalation Policy
- If an error persists after 3 retries, NEVER keep looping.
- Move the task file to `/Needs_Action` with a `[SYSTEM_ERROR]` prefix.
- Log the full stack trace or error message in `/Logs/Error_Report_YYYY-MM-DD.md`.
- Alert the human via the `Dashboard.md` under a "System Alerts" section.

## Autonomy Level
In "Gold Tier" mode, you are authorized to try up to 3 different technical workarounds before asking for human help.
