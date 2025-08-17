@echo off
echo Starting Next.js Frontend...
echo.
echo Make sure you have installed the dependencies:
echo npm install
echo.
echo Frontend will be available at: http://localhost:3000
echo.
cd /d "%~dp0"
npm run dev
pause
