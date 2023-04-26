chcp 65001
schtasks /create /tn RestartOpeRateMonitor /tr "C:\設備稼働率監視ツール_ver1.2\python-3.6.5-embed-win32\bat\restart.bat" /sc MONTHLY /rl highest /F /M "*" /D 1 /ST 09:00

rem schtasks /delete /tn "When Lock" /f
rem schtasks /delete /tn "When unlock" /f

pause
