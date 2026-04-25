---
name: linkedin_manager
description: Automatically generate and post business updates to LinkedIn
---

# LinkedIn Manager Skill 📱

## Purpose
Helps you grow your personal brand and generate sales by posting regular, high-quality content to your LinkedIn profile.

## Workflow

### 1. Identify Topic
- Read **`Business_Goals.md`** to see what we are currently selling/building.
- Check **`Plans/`** or **`Done/`** for recent achievements.

### 2. Draft Post
- Write a professional, punchy post (hook -> body -> CTA).
- Use proper hashtags (e.g., #AI #Automation #FTE).
- Ensure it sounds human!

### 3. Approval Workflow (IMPORTANT)
- Save the drafted post to **`/Pending_Approval/LINKEDIN_POST_[DATE].md`**.
- Do **NOT** post until the file is moved to **`/Approved`**.

### 4. Execute Post (Browser-MCP)
- If a post exists in `/Approved`, start the `browser` server.
- Navigate to `linkedin.com`.
- Logic: Click "Start a post" -> Type text -> Click "Post".

## Rules
- ❌ **NEVER** post without seeing a file in `/Approved`.
- ✅ **ALWAYS** log the LinkedIn URL in `Logs/` after a successful post.
- ✅ If LinkedIn asks for a Login/Captcha, stop and notify the human.
