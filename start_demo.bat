@echo off
echo ===================================================
echo     WasteLink AI - Startup Script
echo ===================================================
echo.

echo Starting the Generative AI Backend (FastAPI)...
start "WasteLink Backend" cmd /k "cd backend && .\venv\Scripts\activate.bat && uvicorn main:app --port 8000"

echo Starting the Interactive Dashboard (Next.js)...
start "WasteLink Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo All services are starting up! 
echo The frontend might take ~10 seconds to compile for the first time.
echo.
echo Press any key to open the dashboard at http://localhost:3000
pause >nul

start http://localhost:3000
