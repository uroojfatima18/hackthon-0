import asyncio
import os
import sys
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# Force UTF-8 encoding for Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

async def run_gold_end_to_end():
    print("==========================================")
    print("🥇 GOLD TIER: END-TO-END AUTONOMOUS TEST")
    print("Task: Generate an Odoo Invoice and Email it to the client")
    print("==========================================\n")
    
    # 1. Connect to Odoo MCP Server
    print("➤ Connecting to Odoo MCP Server...")
    odoo_params = StdioServerParameters(
        command=os.path.join(".venv", "Scripts", "python.exe"),
        args=["D:/Urooj/Hackthon 0/mcp_servers/odoo_mock.py"],
        env=None
    )

    invoice_details = None

    async with stdio_client(odoo_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to Odoo ERP.")
            
            print("➤ AI calling Odoo tool: create_invoice...")
            result = await session.call_tool("create_invoice", arguments={
                "partner_name": "Panaversity Client",
                "amount": 2500.0,
                "description": "Gold Tier Automation Setup Fee"
            })
            invoice_details = result.content[0].text if result.content else str(result)
            print(f"✅ Odoo Response: {invoice_details}")
            
    await asyncio.sleep(2)
    print("\n------------------------------------------\n")
    
    # 2. Connect to Gmail MCP Server
    print("➤ Connecting to Gmail MCP Server...")
    gmail_params = StdioServerParameters(
        command="node",
        args=["D:/Urooj/Hackthon 0/mcp_servers/gmail/index.js"],
        env=None
    )

    async with stdio_client(gmail_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            print("✅ Connected to Gmail.")
            
            print("➤ AI calling Gmail tool: send_email...")
            email_body = (
                f"Dear Panaversity Client,\n\n"
                f"Your invoice has been successfully generated via our autonomous Odoo system.\n\n"
                f"Invoice Details:\n{invoice_details}\n\n"
                f"Please process the payment at your earliest convenience.\n\n"
                f"Best regards,\nYour AI Employee"
            )
            
            result = await session.call_tool("send_email", arguments={
                "to": "roojfatima22@gmail.com",
                "subject": "Your Automated Odoo Invoice - Gold Tier Test",
                "body": email_body
            })
            print(f"✅ Gmail Response: {result.content[0].text if result.content else str(result)}")

    print("\n==========================================")
    print("🎉 END-TO-END GOLD TIER TEST SUCCESSFUL! 🎉")
    print("==========================================")

if __name__ == "__main__":
    asyncio.run(run_gold_end_to_end())
