@echo off
REM OCR Screen Server - MLS Gateway
REM Provides screen capture and OCR text extraction

echo Starting OCR Screen Server...
echo.
echo Requirements:
echo - pillow: pip install pillow
echo - pytesseract: pip install pytesseract
echo - Tesseract-OCR binary: https://github.com/tesseract-ocr/tesseract
echo.

H:\Tools\python.exe "P:\ECHO_PRIME\MLS_CLEAN\PRODUCTION\GATEWAYS\OCR_SCREEN\ocr_screen_http.py"
