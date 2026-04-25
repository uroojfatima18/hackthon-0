"""
GOLD TIER WATCHDOG
Monitors and restarts critical AI Employee processes if they crash.
"""

import subprocess
import time
import os
import sys
import logging
from dotenv import load_dotenv

# Load API keys from .env
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [WATCHDOG] - %(levelname)s - %(message)s'
)
logger = logging.getLogger('Watchdog')

# Configuration: Processes to monitor
PROCESSES = {
    "Gold Orchestrator": ["python", "gold_openrouter_orchestrator.py"],
    "Gmail Watcher": ["python", "watchers/gmail_watcher.py"],
    "File Watcher": ["python", "watchers/filesystem_watcher.py"],
    "Social Poster": ["python", "social_autopost.py"]
}

running_processes = {}

def start_process(name, cmd):
    """Starts a process and returns its handle."""
    logger.info(f"STARTING {name}: {' '.join(cmd)}")
    try:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )
        return proc
    except Exception as e:
        logger.error(f"FAILED to start {name}: {e}")
        return None

def monitor():
    logger.info("=" * 50)
    logger.info("GOLD TIER WATCHDOG STARTED")
    logger.info("Monitoring Orchestrator and Watchers...")
    logger.info("=" * 50)

    for name, cmd in PROCESSES.items():
        running_processes[name] = start_process(name, cmd)

    try:
        while True:
            time.sleep(10)
            for name, proc in running_processes.items():
                if proc is None or proc.poll() is not None:
                    exit_code = proc.poll() if proc else "Never Started"
                    logger.warning(f"ALERT: {name} is DOWN (Exit Code: {exit_code}). Restarting...")
                    running_processes[name] = start_process(name, PROCESSES[name])
    except KeyboardInterrupt:
        logger.info("STOPPING Watchdog...")
        for name, proc in running_processes.items():
            if proc: proc.terminate()
        sys.exit(0)

if __name__ == "__main__":
    monitor()
