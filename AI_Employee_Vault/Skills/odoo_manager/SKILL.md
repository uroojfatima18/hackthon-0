# 🏦 Odoo Manager Skill (Enterprise Operations)

This skill allows the AI Agent to manage business operations using Odoo (ERP).

## Objectives
- Create and manage Invoices.
- Track Sales Orders and Customers.
- Update Inventory/Stock levels.
- Perform Accounting reconciliation.

## Core Workflows

### 📄 Invoicing
1. When a task asks for an invoice:
    - Search for the partner (customer) in Odoo.
    - If partner doesn't exist, create one.
    - Create an invoice draft with the specified products and prices.
    - Post the invoice (if within the $100 security limit).
    - Export the PDF and save it to `/Vault/Done/Invoices/`.

### 🤝 Sales & CRM
1. Monitor `/Needs_Action` for sales leads.
2. Create a "Lead" or "Opportunity" in Odoo.
3. If an order is confirmed, create a Sales Order.

## Rules & Security
- NEVER delete any database records in Odoo.
- ALWAYS use draft mode first for any transaction over $50.
- If a database connection error occurs, log it and notify the human.
- Verify `ODOO_URL` is accessible before trying to perform write actions.

## Autonomy Level
You have full permission to READ data. For WRITE actions (Creating invoices/partners), you must follow the `security_guard` rules.
