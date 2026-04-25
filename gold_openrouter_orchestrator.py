"""
GOLD TIER OPENROUTER ORCHESTRATOR
Replaces paid Claude Code CLI with OpenRouter API.
"""

import time
import logging
from pathlib import Path
from dotenv import load_dotenv
from openrouter_agent import OpenRouterAgent
from audit_logger import AuditLogger

# Load .env
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [GOLD-OR] - %(levelname)s - %(message)s'
)
logger = logging.getLogger('OpenRouterOrchestrator')

class GoldOpenRouterOrchestrator:
    def __init__(self, vault_path: str, check_interval: int = 30):
        self.vault_path = Path(vault_path)
        self.check_interval = check_interval
        
        self.needs_action = self.vault_path / 'Needs_Action'
        self.pending = self.vault_path / 'Pending_Approval'
        self.plans = self.vault_path / 'Plans'
        self.done = self.vault_path / 'Done'
        
        # Initialize Agent and Logger
        self.agent = OpenRouterAgent()
        self.audit = AuditLogger(vault_path, db_path="D:/Urooj/Hackthon 0/audit_logs.db")
        
        # Read Handbook for context
        self.handbook_path = self.vault_path / "Company_Handbook.md"
        self.handbook = self.handbook_path.read_text(encoding='utf-8') if self.handbook_path.exists() else ""

    def process_task(self, task_file: Path):
        """Processes a single task through OpenRouter."""
        logger.info(f"Processing task: {task_file.name}")
        task_content = task_file.read_text(encoding='utf-8')
        
        prompt = (
            f"I have a new task in {task_file.name}:\n\n{task_content}\n\n"
            "Please analyze this and provide:\n"
            "1. A Plan (what steps to take).\n"
            "2. If it's a simple text task, provide the final result content.\n"
            "After answering, I will move this file to /Done or /Pending_Approval."
        )
        
        # Get response from OpenRouter
        response = self.agent.chat(prompt, context=self.handbook)
        
        if response:
            # 1. Save Plan/Result to /Plans
            plan_file = self.plans / f"PLAN_{task_file.name}"
            plan_file.write_text(response, encoding='utf-8')
            logger.info(f"Plan created: {plan_file.name}")
            
            # 2. Log Action
            self.audit.log("task_processed", "OpenRouterAgent", task_file.name, {"plan": plan_file.name}, "success")
            
            # 3. Move original task to Done (or Pending if sensitive)
            if "APPROVAL_REQUIRED" in task_content or "SENSITIVE" in task_content:
                dest = self.pending / task_file.name
            else:
                dest = self.done / task_file.name
            
            task_file.rename(dest)
            logger.info(f"Task moved to {dest.parent.name}")
        else:
            logger.error(f"Failed to get response for {task_file.name}")

    def run(self):
        logger.info("=" * 60)
        logger.info("GOLD OPENROUTER ORCHESTRATOR STARTED")
        logger.info("Autonomy: Enabled (OpenRouter API Mode)")
        logger.info("=" * 60)
        
        try:
            while True:
                # Scan for tasks
                tasks = list(self.needs_action.glob('*.md'))
                if tasks:
                    logger.info(f"Found {len(tasks)} tasks to process.")
                    for task in tasks:
                        self.process_task(task)
                
                time.sleep(self.check_interval)
        except KeyboardInterrupt:
            logger.info("Orchestrator stopped.")

if __name__ == "__main__":
    ORC = GoldOpenRouterOrchestrator(vault_path="D:/Urooj/Hackthon 0/AI_Employee_Vault")
    ORC.run()
