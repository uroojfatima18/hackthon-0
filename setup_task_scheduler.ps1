$action = New-ScheduledTaskAction -Execute "cmd.exe" -Argument "/c ""D:\Urooj\Hackthon 0\start_ai_employee.bat"""
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 30)
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable
Register-ScheduledTask -TaskName "AI_Employee_Orchestrator" -Action $action -Trigger $trigger -Settings $settings -Description "Runs the AI Employee Orchestrator every 30 minutes"
Write-Host "Task 'AI_Employee_Orchestrator' has been successfully created in Windows Task Scheduler!"
Write-Host "It will run start_ai_employee.bat every 30 minutes."
pause
