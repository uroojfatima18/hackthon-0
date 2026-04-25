# 🚀 Autonomous AI Employee (Gold Tier Completed)

Welcome to the **Personal AI Employee Hackathon 2026** project! This repository contains a fully autonomous AI Employee that has successfully achieved the **Bronze, Silver, and Gold Tiers**. It acts as a digital Full-Time Equivalent (FTE) to manage business operations 24/7.

## 🏆 Achievements & Features

### 🥉 Bronze Tier (Foundation)
- **Local-First Architecture:** Uses Obsidian Markdown Vault (`AI_Employee_Vault/`) as the memory and GUI.
- **File System Monitoring:** A Watcher script automatically ingests files from the `DropZone/` to the Vault.
- **Claude Code Integration:** Initial setup of Agent Skills for file processing.

### 🥈 Silver Tier (Functional Assistant)
- **Multi-Watcher System:** Includes `gmail_watcher.py` to autonomously monitor unread/important emails and `filesystem_watcher.py`.
- **OpenRouter Orchestrator:** Transitioned from paid Claude CLI to a native Python Orchestrator (`python_orchestrator.py`) using the free Gemini API via OpenRouter.
- **Human-in-the-Loop (HITL):** AI creates drafts in `Pending_Approval`. Human moves them to `Approved` for execution.
- **MCP Email Server:** Integrates with Gmail MCP Server to actually send approved emails directly from the terminal.
- **LinkedIn Automation:** Playwright script (`post_to_linkedin.py`) to autonomously post achievements to LinkedIn.
- **Task Scheduler:** Configured Windows Task Scheduler to run the AI system in the background automatically.

### 🥇 Gold Tier (Autonomous Employee)
- **Odoo ERP Integration:** Built a Mock Odoo MCP Server (`mcp_servers/odoo_mock.py`) to create partners and draft invoices via AI.
- **Monday Morning CEO Briefing:** Implemented `audit_logic.py` that reads `Business_Goals.md` and generates a weekly executive summary of revenue, tasks, and suggestions.
- **Ralph Wiggum Loop:** The orchestrator continuously scans for complex multi-step tasks in `Needs_Action` and doesn't stop until all sub-tasks (emails, social posts) are drafted.
- **Audit Logging & Error Recovery:** Integrated SQLite (`audit_logs.db`) for tracking every AI action, alongside a `watchdog.py` process to restart failed services.

---

## 📁 Project Structure

- `AI_Employee_Vault/`: Your local Obsidian vault (The AI's Brain/Dashboard).
- `watchers/`: Python scripts monitoring Email and DropZone.
- `mcp_servers/`: Contains the Gmail and Odoo Mock MCP servers.
- `python_orchestrator.py`: The main OpenRouter-native orchestrator script.
- `start_ai_employee.bat`: Master script to launch all Watchers and the Orchestrator simultaneously.
- `audit_logic.py`: Generates the Weekly CEO Briefing.
- `test_odoo.py`: Test script to verify Odoo MCP Server integration.

## 🚀 How to Run

### 1. Configure the Environment
Create a `.env` file in the root directory and add your OpenRouter API Key:
```env
OPENROUTER_API_KEY=your_api_key_here
```

### 2. Start the AI Employee
Run the master batch file to launch the entire system (Watchers + Orchestrator):
```powershell
.\start_ai_employee.bat
```

### 3. Usage
1. **Emails:** Mark an email as Unread & Important in Gmail, and the AI will draft a reply in `Pending_Approval/`.
2. **Tasks:** Drop any text file into the `DropZone/` folder.
3. **Approval:** Move any `.md` file from `Pending_Approval/` to `Approved/` to let the AI execute it (e.g., sending the email or posting the invoice).

---
*Built for the Personal AI Employee Hackathon 2026. Transitioning towards Platinum Tier.*
