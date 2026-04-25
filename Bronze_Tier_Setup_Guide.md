# Personal AI Employee - Bronze Tier Setup Guide
**Estimated Time: 8-12 hours**

## 🎯 What You're Building

A **local AI assistant** that:
- Monitors your Gmail or a folder for new items
- Uses Claude Code to read and process them
- Stores everything in Obsidian (a local markdown vault)
- Can autonomously decide what actions to take

Think of it as your first "junior employee" that handles incoming tasks.

---

## 📋 Bronze Tier Checklist

- [ ] Obsidian vault with Dashboard.md and Company_Handbook.md
- [ ] One working Watcher script (Gmail OR file system monitoring)
- [ ] Claude Code successfully reading from and writing to the vault
- [ ] Basic folder structure: /Inbox, /Needs_Action, /Done
- [ ] All AI functionality implemented as Agent Skills

---

## 🚀 Step-by-Step Setup

### **Step 1: Install Prerequisites** (30 minutes)

#### 1.1 Install Obsidian
- Download from: https://obsidian.md/
- Install and open it
- Skip the tutorial for now

#### 1.2 Verify Claude Code
```bash
# Check if Claude Code is installed
claude --version

# If not installed, install it
npm install -g @anthropic/claude-code
```

#### 1.3 Install Python and UV
```bash
# Check Python version (need 3.13+)
python3 --version

# Install UV (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or on Windows with PowerShell:
irm https://astral.sh/uv/install.ps1 | iex
```

#### 1.4 Install Node.js
- Download from: https://nodejs.org/ (v24+ LTS)
- Install and verify: `node --version`

---

### **Step 2: Create Your Obsidian Vault** (15 minutes)

#### 2.1 Create New Vault
1. Open Obsidian
2. Click "Create new vault"
3. Name it: `AI_Employee_Vault`
4. Choose location: somewhere easy to find (e.g., `~/Documents/AI_Employee_Vault`)
5. Click "Create"

#### 2.2 Note Your Vault Path
```bash
# On Mac/Linux, it might be:
/Users/YOUR_USERNAME/Documents/AI_Employee_Vault

# On Windows:
C:\Users\YOUR_USERNAME\Documents\AI_Employee_Vault
```

**IMPORTANT**: Save this path - you'll need it constantly!

---

### **Step 3: Create Folder Structure** (5 minutes)

In Obsidian, create these folders:

```
AI_Employee_Vault/
├── Inbox/              # Raw incoming items
├── Needs_Action/       # Items requiring processing
├── Done/               # Completed tasks
├── Plans/              # AI-generated plans
├── Skills/             # Agent Skills (we'll create these)
├── Logs/               # Activity logs
└── Config/             # Configuration files
```

**How to create folders in Obsidian:**
1. Right-click in the file explorer (left sidebar)
2. Select "New folder"
3. Name it exactly as shown above
4. Repeat for all folders

---

### **Step 4: Create Core Documents** (20 minutes)

#### 4.1 Create Dashboard.md
In Obsidian, create a new note called `Dashboard.md` in the root:

```markdown
# AI Employee Dashboard
Last Updated: {{date}}

## 📊 Status
- **Active Tasks**: 0
- **Completed Today**: 0
- **Needs Attention**: 0

## 🔥 Priority Items
*No items yet*

## 📥 Recent Activity
*No activity yet*

## ⚙️ System Status
- Watcher: Not Running
- Last Check: Never
- Vault Location: /path/to/your/vault
```

#### 4.2 Create Company_Handbook.md
Create `Company_Handbook.md` in the root:

```markdown
# Company Handbook - AI Employee Rules

## 🎯 My Purpose
I am your personal AI assistant that helps monitor and process incoming tasks.

## 📜 Core Rules

### Communication Style
- Always be professional but friendly
- Use clear, concise language
- Flag anything urgent immediately

### Decision Making
- ✅ **I CAN do automatically**:
  - Read incoming emails/files
  - Create summaries
  - Categorize items by priority
  - Draft responses for your approval

- ⛔ **I MUST ask permission for**:
  - Sending any emails
  - Making purchases
  - Deleting anything
  - Sharing information with others

### Priority Levels
- 🔴 **URGENT**: Requires immediate attention (clients, deadlines)
- 🟡 **IMPORTANT**: Should be handled today
- 🟢 **ROUTINE**: Can be scheduled

### Email Processing Rules
1. Check for keywords: "urgent", "ASAP", "deadline", "invoice"
2. Identify sender importance (clients > general inquiries)
3. Create action item in /Needs_Action
4. Draft response but DON'T send without approval

### Work Hours
- Monitoring: 24/7
- Action recommendations: Only during 9 AM - 6 PM
- Emergency escalation: Any time for URGENT items

## 🚨 Emergency Protocols
If I see:
- "Payment failed"
- "Account locked"
- Client angry
- Legal issues

→ Create file in /Needs_Action with URGENT tag immediately
```

---

### **Step 5: Set Up Python Environment** (15 minutes)

#### 5.1 Create Project Directory
```bash
# Navigate to a good location (NOT inside Obsidian vault)
cd ~/Documents/
mkdir ai_employee_project
cd ai_employee_project
```

#### 5.2 Initialize UV Project
```bash
# Create new Python project
uv init ai-employee
cd ai-employee

# Create virtual environment
uv venv

# Activate it (Mac/Linux):
source .venv/bin/activate

# Or Windows:
.venv\Scripts\activate
```

#### 5.3 Install Required Packages
```bash
# Install packages
uv pip install watchdog python-dotenv pathlib
```

---

### **Step 6: Choose Your Watcher Type** (Decision Point)

**Option A: File System Watcher** (EASIER - Start with this!)
- Monitors a folder on your computer
- When you drop a file, AI processes it
- Great for learning the basics
- No API setup needed

**Option B: Gmail Watcher** (HARDER - Do this second)
- Monitors your Gmail inbox
- Automatically processes emails
- Requires Google API setup
- More realistic "employee" behavior

**👉 RECOMMENDATION**: Start with File System Watcher, get it working, then add Gmail later.

---

### **Step 7A: Build File System Watcher** (30 minutes)

#### 7A.1 Create the Watcher Script

Create file: `filesystem_watcher.py`

```python
"""
File System Watcher - Bronze Tier
Monitors a folder and copies new files to Obsidian vault
"""

import time
import shutil
from pathlib import Path
from datetime import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('FileWatcher')

class FileDropHandler(FileSystemEventHandler):
    """Handles new files dropped in watched folder"""
    
    def __init__(self, vault_path: str, watch_folder: str):
        self.vault_path = Path(vault_path)
        self.watch_folder = Path(watch_folder)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        
        # Ensure folders exist
        self.needs_action.mkdir(exist_ok=True)
        self.inbox.mkdir(exist_ok=True)
        
        logger.info(f"Watching: {watch_folder}")
        logger.info(f"Vault: {vault_path}")
    
    def on_created(self, event):
        """Called when a new file is created"""
        if event.is_directory:
            return
        
        try:
            # Wait a moment for file to finish writing
            time.sleep(1)
            
            source = Path(event.src_path)
            
            # Ignore hidden files and system files
            if source.name.startswith('.'):
                return
            
            logger.info(f"New file detected: {source.name}")
            
            # Copy to Inbox
            inbox_dest = self.inbox / source.name
            shutil.copy2(source, inbox_dest)
            logger.info(f"Copied to Inbox: {source.name}")
            
            # Create metadata file in Needs_Action
            self.create_action_file(source)
            
        except Exception as e:
            logger.error(f"Error processing {source.name}: {e}")
    
    def create_action_file(self, source_file: Path):
        """Create a markdown file in Needs_Action with metadata"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine priority based on filename
        priority = "🟢 ROUTINE"
        if any(word in source_file.name.lower() for word in ['urgent', 'important', 'asap']):
            priority = "🔴 URGENT"
        elif any(word in source_file.name.lower() for word in ['invoice', 'contract', 'proposal']):
            priority = "🟡 IMPORTANT"
        
        content = f"""---
type: file_drop
original_name: {source_file.name}
size: {source_file.stat().st_size} bytes
detected: {timestamp}
priority: {priority}
status: pending
---

# New File Requires Action

## File Details
- **Name**: {source_file.name}
- **Size**: {source_file.stat().st_size:,} bytes
- **Detected**: {timestamp}
- **Priority**: {priority}

## File Location
File copied to: `/Inbox/{source_file.name}`

## Suggested Actions
- [ ] Review file contents
- [ ] Determine appropriate action
- [ ] Process or delegate
- [ ] Move to /Done when complete

## Notes
*Add your notes here*
"""
        
        # Create action file
        action_filename = f"FILE_{source_file.stem}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        action_path = self.needs_action / action_filename
        action_path.write_text(content)
        
        logger.info(f"Created action file: {action_filename}")
        
        # Update dashboard
        self.update_dashboard()
    
    def update_dashboard(self):
        """Update the dashboard with current counts"""
        try:
            needs_action_count = len(list(self.needs_action.glob('*.md')))
            dashboard = self.vault_path / 'Dashboard.md'
            
            if dashboard.exists():
                content = dashboard.read_text()
                # Update the active tasks count (simple replacement)
                content = content.replace(
                    '- **Active Tasks**: 0',
                    f'- **Active Tasks**: {needs_action_count}'
                )
                dashboard.write_text(content)
                logger.info(f"Dashboard updated: {needs_action_count} active tasks")
        except Exception as e:
            logger.error(f"Could not update dashboard: {e}")


def main():
    """Main function to run the watcher"""
    
    # CONFIGURATION - CHANGE THESE PATHS!
    VAULT_PATH = "/Users/YOUR_USERNAME/Documents/AI_Employee_Vault"
    WATCH_FOLDER = "/Users/YOUR_USERNAME/Documents/DropZone"
    
    print("=" * 60)
    print("🤖 AI EMPLOYEE - FILE SYSTEM WATCHER")
    print("=" * 60)
    print(f"📁 Watching: {WATCH_FOLDER}")
    print(f"🗄️  Vault: {VAULT_PATH}")
    print(f"⏰ Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print("Drop files into the watch folder to process them...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    # Create watch folder if it doesn't exist
    Path(WATCH_FOLDER).mkdir(parents=True, exist_ok=True)
    
    # Set up the watcher
    event_handler = FileDropHandler(VAULT_PATH, WATCH_FOLDER)
    observer = Observer()
    observer.schedule(event_handler, WATCH_FOLDER, recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n🛑 Stopping watcher...")
        observer.stop()
    
    observer.join()
    print("✅ Watcher stopped successfully")


if __name__ == "__main__":
    main()
```

#### 7A.2 Configure the Watcher

1. Open `filesystem_watcher.py`
2. Find this section (around line 120):

```python
VAULT_PATH = "/Users/YOUR_USERNAME/Documents/AI_Employee_Vault"
WATCH_FOLDER = "/Users/YOUR_USERNAME/Documents/DropZone"
```

3. Replace with YOUR actual paths:
   - `VAULT_PATH`: The path to your Obsidian vault
   - `WATCH_FOLDER`: Create a new folder anywhere you like (this is where you'll drop files)

#### 7A.3 Test the Watcher

```bash
# Make sure you're in the ai-employee directory
cd ~/Documents/ai_employee_project/ai-employee

# Activate virtual environment if not already active
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate  # Windows

# Run the watcher
python filesystem_watcher.py
```

You should see:
```
============================================================
🤖 AI EMPLOYEE - FILE SYSTEM WATCHER
============================================================
📁 Watching: /Users/YOUR_USERNAME/Documents/DropZone
🗄️  Vault: /Users/YOUR_USERNAME/Documents/AI_Employee_Vault
⏰ Started: 2026-02-12 10:30:00
============================================================
Drop files into the watch folder to process them...
Press Ctrl+C to stop
============================================================
```

#### 7A.4 Test It!

1. Keep the watcher running
2. Open your DropZone folder
3. Create a test file: `test_urgent.txt` with some text
4. Drop it into the DropZone
5. Check Obsidian - you should see:
   - File in `/Inbox`
   - New markdown file in `/Needs_Action`
   - Dashboard updated

---

### **Step 8: Create Your First Agent Skill** (45 minutes)

Agent Skills teach Claude Code how to perform specific tasks automatically. Let's create one!

#### 8.1 Create Skills Folder Structure

```bash
# In your Obsidian vault
mkdir -p Skills/process_file
```

#### 8.2 Create the Skill File

In Obsidian, create: `Skills/process_file/SKILL.md`

```markdown
---
name: process_file
description: Process files from Needs_Action folder, analyze them, and create action plans
---

# File Processing Skill

## Purpose
Automatically process files that appear in the /Needs_Action folder and create actionable plans.

## When to Use This Skill
- User says "process my files" or "check needs action"
- Scheduled task triggers (e.g., every hour)
- User wants to review pending items

## Workflow

### Step 1: Scan Needs_Action Folder
Read all `.md` files in the `/Needs_Action` folder:

```bash
view /path/to/vault/Needs_Action
```

### Step 2: Read Each Action File
For each file found:
1. Read the full content
2. Extract key information:
   - Original filename
   - Priority level
   - File type
   - Metadata

### Step 3: Analyze and Categorize
Determine what type of action is needed:

**Document Types:**
- PDF/Word Doc → "Review document"
- Spreadsheet → "Analyze data"
- Image → "Review image"
- Text file → "Read and process content"
- Unknown → "Determine file type"

**Priority Assessment:**
- 🔴 URGENT → Process immediately, flag for user
- 🟡 IMPORTANT → Add to today's todo list
- 🟢 ROUTINE → Schedule for later

### Step 4: Create Action Plan
For each file, create a plan file in `/Plans`:

```markdown
---
source: /Needs_Action/FILE_xyz.md
priority: URGENT/IMPORTANT/ROUTINE
created: {{timestamp}}
status: pending
---

# Action Plan: [Filename]

## Summary
[Brief description of what this file is]

## Recommended Actions
1. [First action]
2. [Second action]
3. [Third action]

## Timeline
- Deadline: [if urgent]
- Suggested completion: [date/time]

## Related Files
- Original file: /Inbox/[filename]
- Action request: /Needs_Action/[filename]

## Next Steps
[What should happen next]
```

### Step 5: Update Dashboard
After processing all files, update the Dashboard.md with:
- Total files processed
- Urgent items count
- Summary of actions needed

### Step 6: Log Activity
Create an entry in `/Logs/YYYY-MM-DD.json`:

```json
{
  "timestamp": "2026-02-12T10:30:00Z",
  "action": "file_processing",
  "files_processed": 3,
  "urgent_count": 1,
  "important_count": 1,
  "routine_count": 1,
  "status": "completed"
}
```

## Error Handling
- If /Needs_Action is empty → Log "No files to process" and exit gracefully
- If file cannot be read → Log error and continue with next file
- If vault path is wrong → Alert user immediately

## Success Criteria
✅ All files in /Needs_Action have been reviewed
✅ Plan files created in /Plans
✅ Dashboard updated with counts
✅ Activity logged

## Example Usage

User: "Process my incoming files"

Claude executes:
1. Reads /Needs_Action folder
2. Finds 2 files
3. Analyzes each:
   - FILE_invoice_20240212.md (IMPORTANT)
   - FILE_urgent_proposal.md (URGENT)
4. Creates plan for each
5. Updates dashboard
6. Reports: "Processed 2 files: 1 urgent, 1 important. See /Plans for details."
```

---

### **Step 9: Configure Claude Code to Use Skills** (15 minutes)

#### 9.1 Create Claude Code Config

Create a file: `.claude-code-config.json` in your vault:

```json
{
  "skills": {
    "path": "Skills",
    "enabled": true,
    "auto_load": true
  },
  "workspace": {
    "vault_path": "/full/path/to/AI_Employee_Vault",
    "auto_save": true
  }
}
```

#### 9.2 Test the Skill

```bash
# Navigate to your vault
cd /path/to/AI_Employee_Vault

# Start Claude Code in this directory
claude --cwd .

# Or just:
claude
```

In Claude Code, try:
```
User: "Process files in my Needs_Action folder"
```

Claude should:
1. Read the skill
2. Execute the workflow
3. Create plan files
4. Update dashboard

---

### **Step 10: Create the Orchestrator** (30 minutes)

The orchestrator coordinates everything. Create: `orchestrator.py`

```python
"""
Simple Orchestrator for Bronze Tier
Runs the watcher and periodically triggers Claude Code
"""

import subprocess
import time
from pathlib import Path
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Orchestrator')

class SimpleOrchestrator:
    def __init__(self, vault_path: str, check_interval: int = 300):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval  # 5 minutes default
        self.needs_action = self.vault_path / 'Needs_Action'
        
    def check_for_work(self):
        """Check if there are files to process"""
        files = list(self.needs_action.glob('*.md'))
        return len(files) > 0
    
    def trigger_claude(self):
        """Trigger Claude Code to process files"""
        logger.info("Triggering Claude Code to process files...")
        
        try:
            # Call Claude Code with a prompt
            prompt = "Process files in my Needs_Action folder using the process_file skill"
            
            result = subprocess.run(
                ['claude', '--prompt', prompt, '--cwd', str(self.vault_path)],
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode == 0:
                logger.info("✅ Claude Code completed successfully")
                return True
            else:
                logger.error(f"❌ Claude Code error: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            logger.error("⏱️ Claude Code timeout (>2 minutes)")
            return False
        except Exception as e:
            logger.error(f"Error triggering Claude: {e}")
            return False
    
    def run(self):
        """Main orchestration loop"""
        logger.info("=" * 60)
        logger.info("🤖 AI EMPLOYEE ORCHESTRATOR STARTED")
        logger.info(f"📁 Vault: {self.vault_path}")
        logger.info(f"⏰ Check interval: {self.check_interval} seconds")
        logger.info("=" * 60)
        
        try:
            while True:
                # Check if there's work to do
                if self.check_for_work():
                    file_count = len(list(self.needs_action.glob('*.md')))
                    logger.info(f"📥 Found {file_count} files to process")
                    self.trigger_claude()
                else:
                    logger.info("😴 No files to process, sleeping...")
                
                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down orchestrator...")


def main():
    VAULT_PATH = "/Users/YOUR_USERNAME/Documents/AI_Employee_Vault"
    
    orchestrator = SimpleOrchestrator(
        vault_path=VAULT_PATH,
        check_interval=300  # Check every 5 minutes
    )
    
    orchestrator.run()


if __name__ == "__main__":
    main()
```

---

### **Step 11: Run Everything Together** (Test It!)

You now have three components. Here's how to run them:

#### Terminal 1: File Watcher
```bash
cd ~/Documents/ai_employee_project/ai-employee
source .venv/bin/activate
python filesystem_watcher.py
```

#### Terminal 2: Orchestrator
```bash
cd ~/Documents/ai_employee_project/ai-employee
source .venv/bin/activate
python orchestrator.py
```

#### Terminal 3: Manual Claude Code (for testing)
```bash
cd /path/to/AI_Employee_Vault
claude
```

---

### **Step 12: Test the Complete System**

1. **Drop a test file**:
   - Create `urgent_invoice.pdf` (or any file)
   - Drop it in your DropZone

2. **Watch the magic**:
   - Watcher detects it → copies to Inbox → creates action file
   - Orchestrator detects new file → triggers Claude
   - Claude reads skill → processes file → creates plan → updates dashboard

3. **Check Obsidian**:
   - File in `/Inbox`
   - Action file in `/Needs_Action`
   - Plan file in `/Plans`
   - Dashboard updated

---

## 🎉 Bronze Tier Complete!

Congratulations! You now have:

✅ Obsidian vault with Dashboard and Handbook
✅ Working File System Watcher
✅ Claude Code integrated with vault
✅ Basic folder structure
✅ Your first Agent Skill
✅ Orchestrator coordinating everything

## 🚀 What's Next?

**To improve your Bronze setup:**
1. Add more skills (email responses, summarization)
2. Improve priority detection
3. Add more logging
4. Create scheduled tasks

**To reach Silver Tier:**
1. Add Gmail Watcher
2. Add MCP servers
3. Implement Human-in-the-Loop approval
4. Add proper scheduling (cron/Task Scheduler)

---

## 🐛 Troubleshooting

### Watcher not detecting files
- Check the watch folder path is correct
- Make sure the watcher is running
- Try dropping a different file type

### Claude Code not finding vault
- Verify vault path in config
- Make sure you're running from the correct directory
- Check file permissions

### Skills not loading
- Ensure SKILL.md is in correct format
- Check the skills path in config
- Verify skill folder structure

### Orchestrator timing out
- Reduce the Claude Code timeout
- Check if Claude is actually installed
- Try running Claude manually first

---

## 📚 Resources

- Obsidian Help: https://help.obsidian.md
- Claude Code Docs: https://agentfactory.panaversity.org
- Watchdog Docs: https://python-watchdog.readthedocs.io
- UV Docs: https://docs.astral.sh/uv

---

**Need help?** Join the Wednesday Research Meeting on Zoom (details in the hackathon doc)!
