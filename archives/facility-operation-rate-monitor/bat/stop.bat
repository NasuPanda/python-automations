cd /d %~dp0
rem current_pidファイルを参照してpidを取得
for /f "usebackq tokens=*" %%a in (../python-3.6.5/src/temp/current_pid) do @set PROCESS_ID=%%a&goto :exit_for
:exit_for

rem タスクの強制終了
taskkill /F /pid %PROCESS_ID%
