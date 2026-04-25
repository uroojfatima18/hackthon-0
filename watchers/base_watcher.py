import time
import logging
from pathlib import Path
from abc import ABC, abstractmethod

class BaseWatcher(ABC):
    """
    Silver Tier Watcher Parent - Defines the pattern for all bots
    """
    def __init__(self, vault_path: str, check_interval: int = 60):
        self.vault_path = Path(vault_path)
        self.needs_action = self.vault_path / 'Needs_Action'
        self.inbox = self.vault_path / 'Inbox'
        self.check_interval = check_interval
        
        # Ensure folders exist
        self.needs_action.mkdir(parents=True, exist_ok=True)
        self.inbox.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(message)s')
          
    @abstractmethod
    def check_for_updates(self) -> list:
        '''Return list of new items to process'''
        pass
      
    @abstractmethod
    def create_action_file(self, item) -> Path:
        '''Create .md file in Needs_Action folder'''
        pass
      
    def run(self):
        self.logger.info(f'Starting {self.__class__.__name__}...')
        while True:
            try:
                items = self.check_for_updates()
                for item in items:
                    self.create_action_file(item)
            except Exception as e:
                self.logger.error(f'Error in {self.__class__.__name__} loop: {e}')
            time.sleep(self.check_interval)
