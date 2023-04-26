@echo off
chcp 65001
rem %~dp0   :  PWD
rem set     :    変数の代入
rem %変数%  : 変数展開

set embeddable_package_dirname=python-3.10.2
set project_root=src
set work_dir=%~dp0%embeddable_package_dirname%/%project_root%
set python_path=%~dp0%embeddable_package_dirname%/python.exe
set main_script=./main.py

echo Please wait a moment...

cd %work_dir%
%python_path% %main_script%
