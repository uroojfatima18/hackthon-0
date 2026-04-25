"""
🥇 GOLD TIER ORCHESTRATOR
Featuring the 'Ralph Wiggum' loop for autonomous multi-step task completion.
"""

import subprocess
import time
from pathlib import Path
from datetime import datetime
import logging
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()
from audit_logger import AuditLogger

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('GoldOrchestrator')

# Use the full path for claude on Windows
CLAUDE_PATH = r"C:\Users\dell\.local\bin\claude.exe"

class GoldOrchestrator:
    def __init__(self, vault_path: str, check_interval: int = 30, max_loops: int = 3):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.max_loops = max_loops
        
        self.inbox = self.vault_path / 'Inbox'
        self.needs_action = self.vault_path / 'Needs_Action'
        self.pending = self.vault_path / 'Pending_Approval'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        
        # Initialize Audit Logger
        self.audit = AuditLogger(vault_path, db_path="D:/Urooj/Hackthon 0/audit_logs.db")
        
        # Ensure Gold Tier folders exist
        for folder in [self.inbox, self.needs_action, self.pending, self.approved, self.done]:
            folder.mkdir(exist_ok=True)
        
    def trigger_claude(self, prompt: str):
        """Trigger Claude Code and wait for completion."""
        logger.info(f"🤖 Triggering Claude: {prompt[:100]}...")
        try:
            # Using --p flag or similar if available, otherwise standard direct prompt
            # For hackathon, we assume 'claude [prompt]' works non-interactively for basic tasks
            command = [CLAUDE_PATH, prompt]
            result = subprocess.run(
                command,
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=600 # 10 mins for complex Gold tasks
            )
            
            if result.returncode == 0:
                logger.info("✅ Claude finished step.")
                self.audit.log("claude_run", "GoldOrchestrator", "ClaudeCode", {"prompt": prompt}, "success")
                return True
            else:
                logger.error(f"❌ Claude error: {result.stderr}")
                self.audit.log("claude_run", "GoldOrchestrator", "ClaudeCode", {"prompt": prompt, "error": result.stderr}, "error")
                return False
        except Exception as e:
            logger.error(f"Error in trigger_claude: {e}")
            return False

    def ralph_wiggum_loop(self, task_file: Path):
        """
        The Ralph Wiggum Pattern:
        Keep Claude working on a specific file until it moves to /Pending_Approval or /Done.
        """
        logger.info(f"🔄 Starting Ralph Wiggum Loop for: {task_file.name}")
        
        loops = 0
        while task_file.exists() and loops < self.max_loops:
            loops += 1
            logger.info(f"  [Loop {loops}/{self.max_loops}] Processing...")
            
            prompt = (
                f"Work on the task: {task_file.name}. Read its content and use your skills to process it. "
                "If it's a multi-step task, perform the next logical step. "
                "IMPORTANT: If the task is finished, move the file to /Done. "
                "If it requires human approval, move it to /Pending_Approval."
            )
            
            success = self.trigger_claude(prompt)
            if not success:
                logger.warning("  ⚠️ Loop interrupted due to Claude error.")
                break
                
            # Wait a moment for file system to sync
            time.sleep(2)
            
            # Check if it moved
            if not task_file.exists():
                logger.info(f"  ✨ Task {task_file.name} successfully moved/completed!")
                return True
                
        if task_file.exists():
            logger.warning(f"  🛑 Max loops reached for {task_file.name}. Task still in Needs_Action.")
        return False

    def check_and_run_weekly_audit(self):
        """Logic to trigger the Monday morning audit."""
        # Simple check: If today is Monday and we haven't done it yet
        now = datetime.now()
        if now.weekday() == 0: # 0 is Monday
            audit_flag = self.vault_path / "Config" / f"audit_done_{now.strftime('%Y-%m-%d')}.txt"
            if not audit_flag.exists():
                logger.info("📅 Monday detected! Triggering Weekly CEO Briefing...")
                prompt = "Run the Weekly Business Audit using your ceo_briefing skill. Generate the report in /Pending_Approval."
                if self.trigger_claude(prompt):
                    audit_flag.touch()
                    logger.info("✅ Weekly audit completed.")

    def run(self):
        logger.info("=" * 60)
        logger.info("🥇 GOLD TIER ORCHESTRATOR ACTIVE")
        logger.info(f"♻️ Ralph Wiggum Max Loops: {self.max_loops}")
        logger.info("=" * 60)
        
        try:
            while True:
                # 1. Weekly Audit Check
                self.check_and_run_weekly_audit()
                
                # 2. Process Needs_Action (Ralph Wiggum Loop)
                action_files = list(self.needs_action.glob('*.md'))
                for task_file in action_files:
                    self.ralph_wiggum_loop(task_file)

                # 3. Process Approved Actions
                approved_files = list(self.approved.glob('*.md'))
                for app_file in approved_files:
                    logger.info(f"🚀 Executing approved action: {app_file.name}")
                    prompt = f"Executing approved action from {app_file.name}. Follow instructions and move to /Done."
                    if self.trigger_claude(prompt):
                        if app_file.exists(): # Double check cleanup
                            app_file.rename(self.done / app_file.name)

                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("🛑 Gold Orchestrator stopped.")

if __name__ == "__main__":
    ORC = GoldOrchestrator(vault_path="D:/Urooj/Hackthon 0/AI_Employee_Vault")
    ORC.run()
