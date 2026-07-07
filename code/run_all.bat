@echo off
setlocal

REM Update this path if ArcGIS Desktop is installed elsewhere.
set PYTHON_EXE=C:\Python27\ArcGIS10.8\python.exe

"%PYTHON_EXE%" run_all.py

if errorlevel 1 (
    echo.
    echo Pipeline failed.
    pause
    exit /b 1
)

echo.
echo Pipeline completed successfully.
pause
