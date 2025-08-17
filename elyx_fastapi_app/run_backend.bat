@echo off
echo Starting FastAPI Backend...
echo.
echo Make sure you have installed the requirements:
echo pip install -r requirements.txt
echo.
echo Backend will be available at: http://localhost:8080
echo.
cd /d "%~dp0"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
pause
