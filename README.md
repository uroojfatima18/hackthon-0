# 🚀 Autonomous AI Employee 

Welcome to the **Personal AI Employee Hackathon 2026** project! This repository contains a fully autonomous AI Employee that acts as a digital Full-Time Equivalent (FTE) to manage business and personal operations 24/7.

This project is built progressively across four tiers. Below is a detailed breakdown of each tier, its tech stack, and what it does.

---

## 🥉 Bronze Tier: Foundation (Minimum Viable Deliverable)
**Goal:** Establish the core brain and memory of the AI Employee.

### What it does:
- Uses a local Obsidian Markdown folder as its brain and dashboard.
- Monitors a local `DropZone` folder for incoming files or tasks.
- Ingests files automatically and moves them into the AI's `Inbox` and `Needs_Action` folders for processing.
- AI uses defined "Agent Skills" (Markdown files) to understand how to process tasks.

### Tech Stack:
- **Python:** Basic watcher scripts (`filesystem_watcher.py`).
- **Obsidian:** Used as the local GUI and memory store (`AI_Employee_Vault/`).
- **Claude Code CLI:** Used manually as the reasoning engine to process the markdown files.

---

## 🥈 Silver Tier: Functional Assistant
**Goal:** Introduce Human-In-The-Loop (HITL) automation and external integrations.

### What it does:
- **Email Triage & Drafting:** Monitors your Gmail inbox for "Important/Unread" emails and drafts polite, professional replies in the `Pending_Approval` folder.
- **Autonomous Execution:** Once a human moves a draft from `Pending_Approval` to `Approved`, the AI actually sends the email.
- **LinkedIn Automation:** Automatically generates business/achievement posts and publishes them directly to LinkedIn.
- **Background Operations:** Uses Windows Task Scheduler to run continuously in the background.

### Tech Stack:
- **Python Orchestrator:** A custom orchestrator (`python_orchestrator.py`) running in an infinite loop.
- **OpenRouter API (Gemini):** Replaced paid Claude CLI with free/open models for reasoning and drafting.
- **Model Context Protocol (MCP):** Node.js-based Gmail MCP server to securely send emails.
- **Playwright (Python):** For automated browser interactions to post on LinkedIn.

---

## 🥇 Gold Tier: Autonomous Employee
**Goal:** Full-scale autonomous business management, complex reasoning, and ERP integration.

### What it does:
- **Monday Morning CEO Briefing:** Reads `Business_Goals.md` and generates a weekly executive summary of revenue, pending tasks, and cost-optimization suggestions.
- **Odoo ERP Integration:** Connects to an accounting system to autonomously create "Partners" (customers) and generate draft invoices.
- **Ralph Wiggum Loop:** The orchestrator continuously scans for complex, multi-step tasks and loops over them until every sub-task is completed.
- **Audit Logging & Watchdog:** Every AI action is logged for compliance. A watchdog script restarts the system if it crashes.

### Tech Stack:
- **Odoo MCP Server (Python):** Custom mock MCP server exposing Odoo's JSON-RPC endpoints as tools.
- **SQLite Database:** Used by `audit_logger.py` to maintain a secure, immutable log of all AI actions.
- **Complex System Prompts:** Advanced prompt engineering to handle multi-step reasoning.

---

## 💎 Platinum Tier: Production-ish Executive (Always-On Cloud)
**Goal:** Move the local brain to the cloud for true 24/7 autonomous operations.

### What it does:
- **24/7 Cloud Operations:** The AI Orchestrator and Watchers run continuously on a cloud virtual machine.
- **Work-Zone Specialization:** The Cloud AI handles 24/7 triage and drafting, while the Local AI (laptop) handles sensitive approvals and final executions (like payments).
- **Vault Syncing:** The AI's Obsidian brain is kept in sync between the Cloud and Local environments to prevent duplicate work.

### Tech Stack:
- **Git / GitHub:** Used as the synchronization layer between the Cloud and Local Obsidian Vaults.
- **Cloud VMs:** Oracle Cloud Free Tier / AWS EC2 / Render.com to host the daemon processes.
- **HTTPS & Webhooks:** For secure communication between the local and cloud environments.

---

## 📁 Project Structure
- `AI_Employee_Vault/`: Your local Obsidian vault (The AI's Brain/Dashboard).
- `watchers/`: Python scripts monitoring Email and DropZone.
- `mcp_servers/`: Contains the Gmail and Odoo Mock MCP servers.
- `python_orchestrator.py`: The main OpenRouter-native orchestrator script.
- `start_ai_employee.bat`: Master script to launch all Watchers and the Orchestrator simultaneously.
- `audit_logic.py` & `test_odoo.py`: Gold tier execution scripts.

## 🚀 How to Run (Local)
1. Configure `.env` with `OPENROUTER_API_KEY=your_key`.
2. Run `.\start_ai_employee.bat` in PowerShell.
3. Drop tasks in `DropZone/` or mark emails as important to trigger the AI!
