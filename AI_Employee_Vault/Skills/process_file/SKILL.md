---
name: process_file
description: Process files from Needs_Action folder, analyze them, and create action plans
---

# File Processing Skill

## Purpose
Automatically process files that appear in the /Needs_Action folder and create actionable plans.

## When to Use This Skill
- User says "process my files" or "check needs action"
- Scheduled task triggers (e.g., every hour)
- User wants to review pending items

## Workflow

### Step 1: Scan Needs_Action Folder
Read all `.md` files in the `/Needs_Action` folder.

### Step 2: Read Each Action File
For each file found:
1. Read the full content.
2. Extract key information:
   - Original filename
   - Priority level
   - File type
   - Metadata

### Step 3: Analyze and Categorize
Determine what type of action is needed based on file extension and content.

### Step 4: Create Action Plan
For each file, create a plan file in `/Plans` with a summary and recommended actions.

### Step 5: Update Dashboard
After processing all files, update the `Dashboard.md` with:
- Total files processed
- Urgent items count
- Summary of actions needed

### Step 6: Log Activity
Create an entry in `/Logs/YYYY-MM-DD.json` or update the current log file.

## Success Criteria
✅ All files in /Needs_Action have been reviewed
✅ Plan files created in /Plans
✅ Dashboard updated with counts
✅ Activity logged
