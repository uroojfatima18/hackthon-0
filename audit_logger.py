"""
📊 GOLD TIER AUDIT LOGGER
Standardized logging to JSON files and SQLite database.
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
import logging

logger = logging.getLogger('AuditLogger')

class AuditLogger:
    def __init__(self, vault_path: str, db_path: str = "audit_logs.db"):
        self.vault_path = Path(vault_path)
        self.logs_dir = self.vault_path / "Logs"
        self.logs_dir.mkdir(exist_ok=True)
        self.db_path = Path(db_path)
        
        self._init_db()

    def _init_db(self):
        """Initialize SQLite database for auditing."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS audit_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                action_type TEXT,
                actor TEXT,
                target TEXT,
                details TEXT,
                status TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def log(self, action_type, actor, target, details, status="success"):
        """Record an action in both JSON and SQLite."""
        timestamp = datetime.now().isoformat()
        
        log_entry = {
            "timestamp": timestamp,
            "action_type": action_type,
            "actor": actor,
            "target": target,
            "details": details,
            "status": status
        }

        # 1. Save to Daily JSON File
        date_str = datetime.now().strftime("%Y-%m-%d")
        json_file = self.logs_dir / f"{date_str}.json"
        
        current_logs = []
        if json_file.exists():
            try:
                current_logs = json.loads(json_file.read_text(encoding='utf-8'))
            except:
                current_logs = []
        
        current_logs.append(log_entry)
        json_file.write_text(json.dumps(current_logs, indent=2), encoding='utf-8')

        # 2. Save to SQLite
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO audit_logs (timestamp, action_type, actor, target, details, status)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (timestamp, action_type, actor, target, str(details), status))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Error saving to DB: {e}")

        logger.info(f"Audit Logged: {action_type} on {target}")

if __name__ == "__main__":
    # Test logging
    audit = AuditLogger("D:/Urooj/Hackthon 0/AI_Employee_Vault")
    audit.log("test_action", "system", "audit_logger", {"message": "Audit system initialized"})
