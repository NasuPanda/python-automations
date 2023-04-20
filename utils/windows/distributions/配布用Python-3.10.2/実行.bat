@echo off
rem %~dp0 = PWD
rem set = 変数の代入
rem %変数% = 変数展開

chcp 65001
set embeddable_package_dirname=python-3.10.2-embed-amd64
set work_dir=%~dp0%embeddable_package_dirname%
set python_path=%~dp0%embeddable_package_dirname%/python.exe
set main_script=./main.py

echo しばらくお待ち下さい...

cd %work_dir%
%python_path% %main_script%

echo 終了するにはEnterを押すか右上の✕ボタンをクリックして下さい
pause