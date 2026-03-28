# Installation Guide

This repository includes a single comprehensive Windows setup script `setup_full.bat` that prepares a fresh environment for local development.

Quick steps (Windows):

1. Copy the project folder to the target laptop.
2. Open PowerShell or cmd in the project root.
3. Run the script:

```powershell
setup_full.bat
```

What the script does:
- Checks for Python and creates a virtual environment (`venv`).
- Installs Python dependencies from `requirements.txt`.
- Generates a `.env` defaulting to SQLite for quick local setup (or copies `.env.example` if you choose).
- Ensures `media` and `staticfiles` directories exist.
- Runs `python manage.py migrate` and `collectstatic`.
- Optionally creates a Django superuser.

Notes and troubleshooting:
- For production or if you want MySQL, choose the option to copy `.env.example` and edit `.env` with your DB credentials before running migrations.
- If dependency installation fails, ensure build tools and database client libraries (e.g., MySQL dev headers) are installed. On Windows, installing Microsoft Build Tools and the appropriate database client may be required for `mysqlclient`.
- If `createsuperuser --noinput` fails, run `python manage.py createsuperuser` manually and supply credentials interactively.

If you'd like, I can also create a ZIP that packages the repo with the new setup script for easy transfer to other machines—tell me and I'll prepare it.
