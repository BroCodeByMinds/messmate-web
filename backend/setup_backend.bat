@echo off
setlocal

:: Set the path to the virtual environment directory
set VENV_DIR=venv
set REQUIREMENTS_FILE=requirements.txt

echo ----------------------------------------
echo Checking virtual environment...
echo ----------------------------------------

:: Check if venv folder exists
if not exist "%VENV_DIR%\" (
    echo Virtual environment not found. Creating one...
    python -m venv %VENV_DIR%
    if errorlevel 1 (
        echo Failed to create virtual environment.
        exit /b 1
    )
) else (
    echo Virtual environment already exists.
)

:: Activate the virtual environment
echo ----------------------------------------
echo Activating virtual environment...
echo ----------------------------------------
call %VENV_DIR%\Scripts\activate.bat

if errorlevel 1 (
    echo Failed to activate virtual environment.
    exit /b 1
)

:: Install dependencies
if exist "%REQUIREMENTS_FILE%" (
    echo ----------------------------------------
    echo Installing packages from %REQUIREMENTS_FILE%...
    echo ----------------------------------------
    pip install -r %REQUIREMENTS_FILE%
) else (
    echo ERROR: requirements.txt not found!
    exit /b 1
)

echo ----------------------------------------
echo Setup complete.
echo ----------------------------------------

endlocal
pause
