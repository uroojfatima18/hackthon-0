import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from base_watcher import BaseWatcher
from datetime import datetime
from pathlib import Path

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

class GmailWatcher(BaseWatcher):
    def __init__(self, vault_path: str, credentials_path: str, token_path: str = 'token.json'):
        # Check for unread emails every 120 seconds
        super().__init__(vault_path, check_interval=120)
        self.credentials_path = Path(credentials_path)
        self.token_path = Path(token_path)
        self.processed_ids = set()
        self.service = self._authenticate()
          
    def _authenticate(self):
        """Standard OAuth 2.0 flow for Gmail API"""
        creds = None
        if self.token_path.exists():
            creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
            
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_path), SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open(str(self.token_path), 'w') as token:
                token.write(creds.to_json())

        return build('gmail', 'v1', credentials=creds)

    def check_for_updates(self) -> list:
        # Search unread/important messages
        results = self.service.users().messages().list(
            userId='me', q='is:unread is:important'
        ).execute()
        messages = results.get('messages', [])
        # Only return messages we haven't touched this session
        return [m for m in messages if m['id'] not in self.processed_ids]
      
    def create_action_file(self, message) -> Path:
        msg = self.service.users().messages().get(
            userId='me', id=message['id']
        ).execute()
          
        # Extract headers (From, Subject, etc.)
        headers = {h['name']: h['value'] for h in msg['payload']['headers']}
          
        content = f'''---
type: email
from: {headers.get('From', 'Unknown')}
subject: {headers.get('Subject', 'No Subject')}
received: {datetime.now().isoformat()}
priority: high
status: pending
---

## Email Summary
{msg.get('snippet', '')}

## Suggested Actions
- [ ] Read full content via MCP
- [ ] Draft a reply
- [ ] Move to /Done when handled

## Thread ID: {message['id']}
'''
        # Filename safe for Windows
        safe_subject = "".join([c for c in headers.get('Subject', 'No_Subject') if c.isalnum() or c==' ']).strip()[:30]
        filename = f"EMAIL_{message['id']}_{safe_subject}.md"
        
        filepath = self.needs_action / filename
        filepath.write_text(content, encoding='utf-8')
        
        # Log to Inbox as well for long-term record
        self.inbox.mkdir(exist_ok=True)
        (self.inbox / filename).write_text(content, encoding='utf-8')
        
        self.logger.info(f"New Email logged: {headers.get('Subject')}")
        self.processed_ids.add(message['id'])
        return filepath

if __name__ == '__main__':
    # Configuration
    VAULT = "D:/Urooj/Hackthon 0/AI_Employee_Vault"
    CREDS = "D:/Urooj/Hackthon 0/credentials.json"
    
    watcher = GmailWatcher(VAULT, CREDS)
    watcher.run()
