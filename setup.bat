@echo off
REM Setup script for Windows
REM This script initializes the Diabetic Retinopathy System for a fresh installation

echo.
echo ============================================
echo Diabetic Retinopathy System - Setup
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo ✓ Python detected

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed
    pause
    exit /b 1
)

echo ✓ pip detected

REM Create virtual environment
echo.
echo Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed

REM Create .env file if it doesn't exist
echo.
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ✓ .env file created - IMPORTANT: Edit .env with your database credentials
) else (
    echo ✓ .env file already exists
)

REM Create necessary directories
echo.
echo Creating media and staticfiles directories...
if not exist media mkdir media
if not exist media\retina_images mkdir media\retina_images
if not exist media\retina_images\original mkdir media\retina_images\original
if not exist media\retina_images\processed mkdir media\retina_images\processed
echo ✓ Directories created

REM Run migrations
echo.
echo Running database migrations...
python manage.py migrate
if errorlevel 1 (
    echo ERROR: Database migrations failed
    echo Make sure your database is running and credentials in .env are correct
    pause
    exit /b 1
)
echo ✓ Database migrations completed

REM Collect static files
echo.
echo Collecting static files...
python manage.py collectstatic --noinput
if errorlevel 1 (
    echo WARNING: Failed to collect static files (non-critical)
)
echo ✓ Static files collected

REM Create superuser (optional)
echo.
echo.
set /p create_user="Do you want to create a superuser account now? (y/n): "
if /i "%create_user%"=="y" (
    python manage.py createsuperuser
)

REM Display next steps
echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next Steps:
echo 1. Edit .env file with your database credentials if needed
echo 2. Start the development server:
echo    python manage.py runserver
echo.
echo 3. Access the application at:
echo    http://127.0.0.1:8000/
echo.
echo 4. Login with the superuser account you created
echo.
echo ============================================
echo.
pause
