@echo off

:: Navigate to the project directory
cd /d "D:\Urooj\Hackthon 0"

:: Check if the virtual environment exists
if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment not found. Please run 'uv sync' first.
    pause
    exit /b 1
)

echo [INFO] Starting AI Employee Services...

:: Start the File System Watcher in a new minimized window
start "FS_Watcher" /min ".venv\Scripts\python.exe" "watchers\filesystem_watcher.py"

:: Start the Gmail Watcher in a new minimized window
start "Gmail_Watcher" /min ".venv\Scripts\python.exe" "watchers\gmail_watcher.py"

:: Start the Orchestrator in the current window (or a new one)
:: We'll keep this one visible so you can see the reasoning loop
echo [INFO] Starting Python-Native Orchestrator...
".venv\Scripts\python.exe" "python_orchestrator.py"

pause