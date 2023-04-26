chcp 65001
rem タスクスケジューラより起動する前提なのでフルパスを記述しておく
rem フルパスを記述したくない場合、タスクスケジューラ側に作業ディレクトリの設定を加える

call C:\設備稼働率監視ツール_ver1.2\python-3.6.5-embed-win32\bat\stop.bat
call C:\設備稼働率監視ツール_ver1.2\python-3.6.5-embed-win32\bat\exec_vbs_wrapper.bat

pause