echo off
chcp 65001
rem このファイルの位置を作業ディレクトリに
rem 必要に応じて変更すること (特に python.exe はフルパスでなければ動かない事が多い)
cd %~dp0%
cd ../python-3.6.5/src
python.exe main.py
pause
