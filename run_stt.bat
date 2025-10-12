@echo off
echo Installing dependencies...
H:\Tools\python.exe -m pip install -r E:\ECHO_XV4\MLS\stt_requirements.txt

echo.
echo Starting Speech-to-Claude...
echo.
H:\Tools\python.exe E:\ECHO_XV4\MLS\speech_to_claude.py
pause
