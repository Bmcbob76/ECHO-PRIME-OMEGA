@echo off
echo ====================================
echo  REINSTALLING PhD AGENT DEPENDENCIES
echo ====================================
echo.

echo Uninstalling old versions...
H:\Tools\python.exe -m pip uninstall -y openai pydantic typing-extensions

echo.
echo Installing compatible versions...
H:\Tools\python.exe -m pip install --upgrade pip
H:\Tools\python.exe -m pip install -r E:\ECHO_XV4\MLS\agents\requirements.txt

echo.
echo ====================================
echo  INSTALLATION COMPLETE
echo ====================================
echo.
pause
