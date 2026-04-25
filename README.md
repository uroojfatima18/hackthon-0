# AI Employee - Bronze Tier Complete 🚀

Congratulations! Your Bronze Tier setup is ready.

## 📁 Project Structure
- `AI_Employee_Vault/`: Your Obsidian vault.
  - `Dashboard.md`: Your system dashboard.
  - `Company_Handbook.md`: Rules for your AI employee.
  - `Needs_Action/`: Where files waiting for processing go.
  - `Inbox/`: Where raw files are stored.
  - `Done/`: Where processed tasks are moved.
  - `Skills/`: Agent Skills for Claude Code.
- `watchers/filesystem_watcher.py`: Monitors the `DropZone` folder.
- `orchestrator.py`: Coordinates the watcher and Claude Code.
- `DropZone/`: Drop your files here!

## 🚀 How to Run

### 1. Start the Watcher
Open a terminal and run:
```bash
python watchers/filesystem_watcher.py
```

### 2. Start the Orchestrator
Open another terminal and run:
```bash
python orchestrator.py
```

### 3. Test it!
1. Drop a file (e.g., `urgent_invoice.txt`) into the `DropZone` folder.
2. Watch it disappear and reappear in `AI_Employee_Vault/Inbox`.
3. An action record will appear in `AI_Employee_Vault/Needs_Action`.
4. The Orchestrator will detect the new file and trigger Claude Code (ensure `claude` is installed and logged in).
5. Claude will use the `process_file` skill to create a plan in `AI_Employee_Vault/Plans`.

## 🛠️ Requirements
- Python 3.13+
- Node.js v24+
- Claude Code (`npm install -g @anthropic/claude-code`)
- Obsidian

---
*Built for the Personal AI Employee Hackathon 2026*
