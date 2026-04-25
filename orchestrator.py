"""
Silver Tier Orchestrator
Enhanced with Human-in-the-Loop (HITL) monitoring for Approved actions.
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

# Use the full path for claude on Windows to avoid path issues
CLAUDE_PATH = r"C:\Users\dell\.local\bin\claude.exe"

class SilverOrchestrator:
    def __init__(self, vault_path: str, check_interval: int = 30):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        self.needs_action = self.vault_path / 'Needs_Action'
        self.approved = self.vault_path / 'Approved'
        self.done = self.vault_path / 'Done'
        
        # Ensure folders exist
        self.approved.mkdir(exist_ok=True)
        self.done.mkdir(exist_ok=True)
        
    def check_for_needs_action(self):
        """Check if there are new items to analyze"""
        files = list(self.needs_action.glob('*.md'))
        return len(files) > 0

    def check_for_approved_actions(self):
        """Check if user has approved any pending actions"""
        files = list(self.approved.glob('*.md'))
        return len(files) > 0
    
    def trigger_claude(self, prompt: str):
        """Trigger Claude Code with a specific instruction"""
        logger.info(f"Triggering Claude: {prompt[:50]}...")
        
        try:
            # Using full path for reliability
            command = [CLAUDE_PATH, prompt]
            result = subprocess.run(
                command,
                cwd=str(self.vault_path),
                capture_output=True,
                text=True,
                encoding='utf-8',
                timeout=300
            )
            
            if result.returncode == 0:
                logger.info("✅ Claude Code completed successfully")
                return True
            else:
                logger.error(f"❌ Claude Code error: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Error triggering Claude: {e}")
            return False
    
    def run(self):
        """Main Silver Tier loop"""
        logger.info("=" * 60)
        logger.info("🥈 SILVER TIER ORCHESTRATOR STARTED (V2 - Full Path)")
        logger.info(f"📁 Vault: {self.vault_path}")
        logger.info(f"⏰ Check interval: {self.check_interval} seconds")
        logger.info("=" * 60)
        
        try:
            while True:
                # Heartbeat to show it's alive
                # logger.info("💓 Orchestrator Heatbeat: Checking for tasks...")
                
                # 1. Process New Items (Analyze & Draft)
                if self.check_for_needs_action():
                    file_count = len(list(self.needs_action.glob('*.md')))
                    logger.info(f"📥 Found {file_count} items to process")
                    prompt = "Process all files in /Needs_Action using process_file and silver_safety skills. Draft any sensitive actions into /Pending_Approval. Do not execute them yet."
                    self.trigger_claude(prompt)

                # 2. Execute Approved Actions
                if self.check_for_approved_actions():
                    approved_files = list(self.approved.glob('*.md'))
                    logger.info(f"✅ Found {len(approved_files)} approved actions!")
                    
                    for app_file in approved_files:
                        logger.info(f"🚀 Executing approved action: {app_file.name}")
                        prompt = f"Executing approved action from {app_file.name}. Read the file content, perform the action using appropriate tools, and then move this file to /Done."
                        if self.trigger_claude(prompt):
                            # Ensure cleanup if Claude somehow missed it
                            if app_file.exists():
                                dest = self.done / app_file.name
                                # Handle filename conflicts
                                if dest.exists():
                                    dest = self.done / f"{app_file.stem}_{int(time.time())}.md"
                                app_file.rename(dest)

                # Wait before next check
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            logger.info("\n🛑 Shutting down Silver orchestrator...")


def main():
    VAULT_PATH = "D:/Urooj/Hackthon 0/AI_Employee_Vault"
    
    # Check every 30 seconds
    orchestrator = SilverOrchestrator(
        vault_path=VAULT_PATH,
        check_interval=30
    )
    
    orchestrator.run()


if __name__ == "__main__":
    main()
