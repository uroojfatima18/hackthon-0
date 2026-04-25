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
            
            # Delete from DropZone after processing
            source.unlink()
            logger.info(f"Removed from DropZone: {source.name}")
            
        except Exception as e:
            logger.error(f"Error processing {source.name}: {e}")
    
    def create_action_file(self, source_file: Path):
        """Create a markdown file in Needs_Action with metadata"""
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Determine priority based on filename
        priority = "[ROUTINE]"
        if any(word in source_file.name.lower() for word in ['urgent', 'important', 'asap']):
            priority = "[URGENT]"
        elif any(word in source_file.name.lower() for word in ['invoice', 'contract', 'proposal']):
            priority = "[IMPORTANT]"
        
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
        action_filename = f"ACTION_{source_file.stem}.md"
        action_path = self.needs_action / action_filename
        action_path.write_text(content, encoding='utf-8')
        
        logger.info(f"Created action file: {action_filename}")
        
        # Update dashboard
        self.update_dashboard()
    
    def update_dashboard(self):
        """Update the dashboard with current counts"""
        try:
            needs_action_count = len(list(self.needs_action.glob('*.md')))
            dashboard = self.vault_path / 'Dashboard.md'
            
            if dashboard.exists():
                content = dashboard.read_text(encoding='utf-8')
                # Update the active tasks count (simple replacement)
                # We'll use a regex-like approach or just find and replace the line
                lines = content.splitlines()
                for i, line in enumerate(lines):
                    if '- **Active Tasks**:' in line:
                        lines[i] = f'- **Active Tasks**: {needs_action_count}'
                        break
                dashboard.write_text('\n'.join(lines), encoding='utf-8')
                logger.info(f"Dashboard updated: {needs_action_count} active tasks")
        except Exception as e:
            logger.error(f"Could not update dashboard: {e}")


def main():
    """Main function to run the watcher"""
    
    # CONFIGURATION
    VAULT_PATH = "D:/Urooj/Hackthon 0/AI_Employee_Vault"
    WATCH_FOLDER = "D:/Urooj/Hackthon 0/DropZone"
    
    print("=" * 60)
    print("AI EMPLOYEE - FILE SYSTEM WATCHER")
    print("=" * 60)
    print(f"File Watching: {WATCH_FOLDER}")
    print(f"Vault Path: {VAULT_PATH}")
    print(f"Started At: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
        print("\n\nStopping watcher...")
        observer.stop()
    
    observer.join()
    print("Watcher stopped successfully")


if __name__ == "__main__":
    main()