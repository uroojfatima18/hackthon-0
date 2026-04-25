# 🥈 Silver Tier: Functional Assistant - Master Plan

Based on the [Personal AI Employee Hackathon 2026 Blueprint](file:///D:/Urooj/Hackthon%200/Personal%20AI%20Employee%20Hackathon%200_%20Building%20Autonomous%20FTEs%20in%202026.md), we are now transitioning from **Observation** (Bronze) to **Action** (Silver).

## 🎯 Silver Tier Goals
1. **Human-in-the-Loop (HITL)**: AI can't act without your permission (Safety First).
2. **Two+ Watchers**: Monitoring Gmail and/or WhatsApp/LinkedIn.
3. **External Actions**: Sending emails via MCP (Model Context Protocol).
4. **Auto-Posting**: Generating and posting content to LinkedIn.
5. **Advanced Reasoning**: Using `Plan.md` files for multi-step tasks.

---

## 📅 Phase 1: Human-in-the-Loop (HITL) Workflow
**Status: COMPLETED ✅**
- [x] Create `/Pending_Approval`, `/Approved`, and `/Rejected` folders in Vault. ✓
- [x] Create `Safety_Skill.md`: Teaches AI to wait for approval before acting. ✓
- [x] Update `orchestrator.py`: Monitor `/Approved` and execute tasks. ✓

## 📅 Phase 2: Action Hands (MCP Servers)
**Status: COMPLETED ✅**
- [x] Set up `email-mcp`: For sending Gmails directly from Claude Code. ✓
- [x] Set up `browser-mcp`: For navigating websites (LinkedIn/WhatsApp). ✓
- [x] Update `.claude-code-config.json` with MCP server paths. (Configured directly in Claude config) ✓

## 📅 Phase 3: Communication Watchers (Gmail)
**Status: COMPLETED ✅**
- [x] Create `gmail_watcher.py`: Scan for important emails and create action files. ✓
- [x] Configure `credentials.json` for Google Cloud API. ✓

## 📅 Phase 4: Business Outreach (LinkedIn)
**Status: COMPLETED ✅**
- [x] Create `LinkedIn_Skill.md`: Write sales posts based on your business goals. ✓
- [x] Automate posting workflow using `browser-mcp` (or Playwright). ✓

## 📅 Phase 5: Scheduling & Automation
**Status: COMPLETED ✅**
- [x] Set up Windows Task Scheduler to run the system every 30-60 minutes (`setup_task_scheduler.ps1` created). ✓
- [x] Final Integration Test: File/Gmail arrives -> AI drafts response -> You approve -> AI sends. ✓

---
*Silver Tier Leveling up...*
