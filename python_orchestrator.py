import os
import time
import json
import asyncio
from pathlib import Path
import logging
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('PyOrchestrator')

VAULT_PATH = Path("D:/Urooj/Hackthon 0/AI_Employee_Vault")
NEEDS_ACTION = VAULT_PATH / "Needs_Action"
PENDING_APPROVAL = VAULT_PATH / "Pending_Approval"
APPROVED = VAULT_PATH / "Approved"
DONE = VAULT_PATH / "Done"

# Create directories if they don't exist
for folder in [NEEDS_ACTION, PENDING_APPROVAL, APPROVED, DONE]:
    folder.mkdir(exist_ok=True, parents=True)

# Important: Read OPENROUTER API KEY from environment
api_key = os.environ.get("OPENROUTER_API_KEY")

try:
    if api_key:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
    else:
        logger.error("Failed to initialize OpenRouter Client. Did you set OPENROUTER_API_KEY?")
        client = None
except Exception as e:
    logger.error(f"Error: {e}")
    client = None

def process_needs_action():
    if not client:
        return
        
    for md_file in NEEDS_ACTION.glob("*.md"):
        content = md_file.read_text('utf-8')
        logger.info(f"Processing new item: {md_file.name}")
        
        prompt = f"""You are an autonomous AI Employee (Silver Tier). You read incoming tasks and draft responses.
Current File Name: {md_file.name}
Content of File:
{content}

Please analyze the email or task above. 
If it is an email, draft a polite, professional reply to the sender answering their request or acknowledging the email.
Provide ONLY the draft content of the email. Do not add any conversational filler.
"""     
        try:
            response = client.chat.completions.create(
                model='google/gemini-2.5-flash', # Or any OpenRouter model
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
            )
            reply_text = response.choices[0].message.content
            
            draft_content = f"---\ntype: draft_approval\ntarget_action: send_email\noriginal_file: {md_file.name}\n---\n\n### Proposed Reply\n{reply_text}\n\n### Original Content Context\n{content[:500]}..."
            
            # Save to pending approval
            draft_name = PENDING_APPROVAL / f"APPROVAL_REQUIRED_{md_file.name}"
            draft_name.write_text(draft_content, encoding='utf-8')
            logger.info(f"Draft created and sent to human for permission: {draft_name.name}")
            
            # Move original out of the way
            md_file.rename(DONE / md_file.name)
        except Exception as e:
            logger.error(f"Error calling OpenRouter: {e}")

async def execute_approved():
    if not client:
        return
        
    approved_files = list(APPROVED.glob("*.md"))
    if not approved_files:
        return

    logger.info(f"Executing {len(approved_files)} approved actions using MCP server...")
    
    # Point directly to the Email MCP Setup
    server_params = StdioServerParameters(
        command="node",
        args=["D:/Urooj/Hackthon 0/mcp_servers/gmail/index.js"],
        env=None
    )

    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                for app_file in approved_files:
                    content = app_file.read_text('utf-8')
                    logger.info(f"Extracting parameters for executing: {app_file.name}")
                    
                    json_prompt = f"""You are an executor agent. 
Below is an approved file. 
Extract the recipient email ('to'), the 'subject', and the 'body' of the reply.
File content:
{content}
Respond strict JSON exactly like {{"to": "...", "subject": "...", "body": "..."}}. NO Markdown formatting, just JSON.
"""                 
                    response = client.chat.completions.create(
                        model='google/gemini-2.5-flash',
                        messages=[{"role": "user", "content": json_prompt}],
                        response_format={ "type": "json_object" },
                        max_tokens=4000,
                    )
                    
                    try:
                        args = json.loads(response.choices[0].message.content)
                        logger.info(f"Calling MCP Tool 'send_email' with Subject: {args.get('subject')}")
                        
                        # EXECUTE PROXY VIA MCP SERVER
                        result = await session.call_tool("send_email", arguments=args)
                        logger.info(f"MCP Action Completed: {result.content[0].text if result.content else result}")
                        
                        # Move to done
                        dest = DONE / app_file.name
                        if dest.exists():
                            dest = DONE / f"{app_file.stem}_{int(time.time())}.md"
                        app_file.rename(dest)
                        
                    except Exception as e:
                        logger.error(f"Failed to execute MCP action for {app_file.name}: {e}")
    except Exception as e:
        logger.error(f"Failed to connect to MCP Server: {e}")

class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"AI Employee Orchestrator is running!")

def start_health_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    logger.info(f"Health check server running on port {port}")
    server.serve_forever()

async def main():
    # Start the web server in a background thread for Render
    threading.Thread(target=start_health_server, daemon=True).start()
    
    logger.info("==========================================")
    logger.info("OPENROUTER-NATIVE AI EMPLOYEE HAS STARTED")
    logger.info("Watching /Needs_Action for new tasks...")
    logger.info("Watching /Approved for your signed-off actions...")
    logger.info("==========================================")
    
    while True:
        process_needs_action()
        await execute_approved()
        await asyncio.sleep(15) # Pulse every 15 seconds

if __name__ == "__main__":
    asyncio.run(main())
