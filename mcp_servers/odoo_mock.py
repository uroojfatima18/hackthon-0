import json
from pathlib import Path
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP Server
mcp = FastMCP("Odoo Mock ERP")

# In-memory database to act like Odoo
DB_FILE = Path("odoo_mock_db.json")

def load_db():
    if DB_FILE.exists():
        return json.loads(DB_FILE.read_text())
    return {"invoices": [], "partners": []}

def save_db(db):
    DB_FILE.write_text(json.dumps(db, indent=2))

@mcp.tool()
def create_partner(name: str, email: str, company: str = "") -> str:
    """Create a new customer/partner in Odoo CRM"""
    db = load_db()
    partner_id = len(db["partners"]) + 1
    partner = {"id": partner_id, "name": name, "email": email, "company": company}
    db["partners"].append(partner)
    save_db(db)
    return f"✅ Partner created successfully in Odoo: {name} (ID: {partner_id})"

@mcp.tool()
def create_invoice(partner_name: str, amount: float, description: str) -> str:
    """Create a new draft invoice in Odoo Accounting"""
    db = load_db()
    invoice_id = len(db["invoices"]) + 1
    invoice = {
        "id": invoice_id, 
        "number": f"INV/2026/000{invoice_id}",
        "partner": partner_name, 
        "amount": amount, 
        "description": description, 
        "status": "draft"
    }
    db["invoices"].append(invoice)
    save_db(db)
    return f"✅ Invoice {invoice['number']} created as DRAFT for {partner_name} (${amount})."

@mcp.tool()
def get_pending_invoices() -> str:
    """Get all draft invoices that need approval"""
    db = load_db()
    drafts = [inv for inv in db["invoices"] if inv["status"] == "draft"]
    if not drafts:
        return "No pending invoices."
    return json.dumps(drafts, indent=2)

if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    print("Odoo Mock MCP Server is starting...")
    mcp.run()
