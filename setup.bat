@echo off

set CD=%cd%

rem 파이썬 경로로 이동
C:
cd C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python39_64

rem pdfminer 설치.
python.exe -m pip install -r %CD%\requirements.txt