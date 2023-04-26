rem 埋め込みPythonが入ったフォルダ名
set python_folder=python-3.10.2
rem python.exeのフルパス
set python_exe_path=%~dp0%python_folder%/python.exe
rem インストール対象のパッケージ
set packages=openpyxl pandas

%python_exe_path% -m pip install %packages%
%python_exe_path% -m pip list

pause
