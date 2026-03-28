@echo off
REM Comprehensive setup script for Windows (portable installer)
REM - Creates and activates a virtualenv
REM - Installs dependencies from requirements.txt
REM - Creates a .env (defaults to SQLite) or copies .env.example
REM - Creates media folders, runs migrations, collects static, optional superuser

echo.
echo ============================================
echo Diabetic Retinopathy System - Full Setup
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

REM Create virtual environment if missing
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo ✓ Virtual environment created
) else (
    echo ✓ Virtual environment already exists
)

REM Activate virtual environment
echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Upgrade pip and install requirements
echo.
echo Upgrading pip and installing dependencies...
python -m pip install --upgrade pip wheel setuptools >nul 2>&1
if exist requirements.txt (
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ERROR: Failed to install Python dependencies
        pause
        exit /b 1
    )
    echo ✓ Dependencies installed
) else (
    echo WARNING: requirements.txt not found. Please add it before running this script.
)

REM Create .env if not present
echo.
if not exist .env (
    echo No .env file found. Choose database option:
    set /p use_sqlite="Use SQLite (recommended for local/testing) ? (Y/n): "
    if /i "%use_sqlite%"=="" set use_sqlite=Y
    if /i "%use_sqlite%"=="Y" (
        echo Creating .env configured for SQLite...
        > .env (
            echo SECRET_KEY=secret-change-me
            echo DEBUG=True
            echo DB_ENGINE=django.db.backends.sqlite3
            echo DB_NAME=db.sqlite3
            echo DB_USER=
            echo DB_PASSWORD=
            echo DB_HOST=
            echo DB_PORT=
            echo ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
        )
        echo ✓ .env created (SQLite). Edit .env if needed.
    ) else (
        if exist .env.example (
            copy .env.example .env >nul
            echo ✓ .env created from .env.example - Edit it with your DB credentials
        ) else (
            echo WARNING: .env.example not found. Creating minimal .env
            > .env (
                echo SECRET_KEY=secret-change-me
                echo DEBUG=True
                echo DB_ENGINE=django.db.backends.sqlite3
                echo DB_NAME=db.sqlite3
                echo ALLOWED_HOSTS=localhost,127.0.0.1
            )
            echo ✓ Minimal .env created
        )
    )
) else (
    echo ✓ .env already exists
)

REM Create necessary directories
echo.
echo Creating media and staticfiles directories...
if not exist media mkdir media
if not exist media\retina_images mkdir media\retina_images
if not exist media\retina_images\original mkdir media\retina_images\original
if not exist media\retina_images\processed mkdir media\retina_images\processed
if not exist staticfiles mkdir staticfiles
echo ✓ Directories ensured

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
) else (
    echo ✓ Static files collected
)

REM Optional superuser creation
echo.
set /p create_user="Do you want to create a superuser account now? (y/n): "
if /i "%create_user%"=="y" (
    echo Enter superuser details. Leave blank to cancel.
    set /p su_username="Username: "
    if "%su_username%"=="" (
        echo Skipping superuser creation.
    ) else (
        set /p su_email="Email: "
        set /p su_password="Password (input will be visible): "
        if "%su_password%"=="" (
            echo Password empty — skipping create.
        ) else (
            set DJANGO_SUPERUSER_USERNAME=%su_username%
            set DJANGO_SUPERUSER_EMAIL=%su_email%
            set DJANGO_SUPERUSER_PASSWORD=%su_password%
            python manage.py createsuperuser --noinput
            if errorlevel 1 (
                echo ERROR: createsuperuser failed. Try running `python manage.py createsuperuser` manually.
            ) else (
                echo ✓ Superuser created
            )
        )
    )
)

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo Next Steps:
echo 1. If using a production DB, edit .env with proper credentials.
echo 2. Start the development server: python manage.py runserver
echo 3. Access the application at: http://127.0.0.1:8000/
echo.
pause
