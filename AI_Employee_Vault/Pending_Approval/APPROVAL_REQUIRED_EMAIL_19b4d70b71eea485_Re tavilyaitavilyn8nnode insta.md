---
type: draft_approval
target_action: send_email
original_file: EMAIL_19b4d70b71eea485_Re tavilyaitavilyn8nnode insta.md
---

### Proposed Reply
Subject: Re: [tavily-ai/tavily-n8n-node] installations problem (Issue #28)

Dear May Ramati Kroitero,

Thank you for bringing this issue to our attention. We understand that you're encountering an installation problem with the `@tavily/n8n-nodes-tavily` package, likely due to a conflict with a previously installed version.

To resolve this, please try the following steps:

1.  **Uninstall the existing package:**
    ```bash
    npm uninstall @tavily/n8n-nodes-tavily
    ```
    or
    ```bash
    yarn remove @tavily/n8n-nodes-tavily
    ```
    (depending on your package manager)

2.  **Clear your package manager's cache:**
    For npm:
    ```bash
    npm cache clean --force
    ```
    For yarn:
    ```bash
    yarn cache clean
    ```

3.  **Reinstall the package:**
    ```bash
    npm install @tavily/n8n-nodes-tavily
    ```
    or
    ```bash
    yarn add @tavily/n8n-nodes-tavily
    ```

If you are installing it within n8n, please ensure that you are following the official n8n documentation for installing custom nodes, which usually involves using the `npm install` command from within your n8n directory or the specific n8n UI installation process.

If the problem persists after following these steps, please provide us with more details about your environment, such as:

*   Operating System
*   Node.js version
*   n8n version
*   Any specific error messages you are receiving during installation

This information will help us diagnose the issue further.

Thank you for your patience.

Best regards,

[Your Name/Support Team]

### Original Content Context
---
type: email
from: May Ramati Kroitero <notifications@github.com>
subject: Re: [tavily-ai/tavily-n8n-node] installations problem (Issue #28)
received: 2026-04-25T16:41:17.277912
priority: high
status: pending
---

## Email Summary
MayRamati left a comment (tavily-ai/tavily-n8n-node#28) It looks like the issue is caused by a conflict with a previously installed version of the @tavily/n8n-nodes-tavily package. To resolve it:

## Suggested Actions
- [ ] Read full content via MCP
- [ ] Draft a re...