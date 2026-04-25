import asyncio
import json
import os
from pathlib import Path
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def run_odoo_test():
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("AI Employee: Connecting to Odoo ERP (Mock)...")
    
    # Connect to our Mock Odoo MCP Server
    server_params = StdioServerParameters(
        command=os.path.join(".venv", "Scripts", "python.exe"),
        args=["D:/Urooj/Hackthon 0/mcp_servers/odoo_mock.py"],
        env=None
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ AI Employee: Connected to Odoo successfully!")
            
            print("\n🤖 AI Employee: Task - Create Customer 'Alex Corp' & Generate $1500 Invoice.")
            
            # Step 1: AI calls create_partner
            print("➤ AI is calling Odoo tool: create_partner...")
            result1 = await session.call_tool("create_partner", arguments={
                "name": "Alex Corp",
                "email": "alex@alexcorp.com",
                "company": "Alex Corporation"
            })
            print(f"Odoo Response: {result1.content[0].text if result1.content else result1}")
            
            await asyncio.sleep(2)
            
            # Step 2: AI calls create_invoice
            print("➤ AI is calling Odoo tool: create_invoice...")
            result2 = await session.call_tool("create_invoice", arguments={
                "partner_name": "Alex Corp",
                "amount": 1500.0,
                "description": "Hackathon AI Consulting Services"
            })
            print(f"Odoo Response: {result2.content[0].text if result2.content else result2}")
            
            await asyncio.sleep(2)
            
            # Step 3: Check Database
            print("\n📊 Checking Odoo Database (odoo_mock_db.json):")
            db_content = Path("odoo_mock_db.json").read_text()
            print(json.dumps(json.loads(db_content), indent=2))
            
if __name__ == "__main__":
    asyncio.run(run_odoo_test())
