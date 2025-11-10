@echo off
echo Installing EPCP30 dependencies...
pip install mcp psutil anthropic python-dotenv fastapi uvicorn --upgrade
echo.
echo ? Dependencies installed!
pause
