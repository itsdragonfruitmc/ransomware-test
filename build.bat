@echo off
title Python to EXE Builder
color 0A

echo ==============================
echo       Python EXE Builder
echo ==============================
echo.

set /p PYFILE=Enter bosd.py:

if not exist "minecraft free.py" (
echo.
echo ERROR: File "bosd.py" was not found.
pause
exit /b 1
)

echo.
echo Installing/updating PyInstaller...
python -m pip install --upgrade pyinstaller

echo.
echo Building EXE...
python -m PyInstaller --onefile --clean "%PYFILE%"

echo.
echo ==============================
echo Build finished!
echo EXE is located in the "dist" folder.
echo ==============================
pause
