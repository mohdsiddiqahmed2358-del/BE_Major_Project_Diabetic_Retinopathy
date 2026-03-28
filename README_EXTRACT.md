Diabetic Retinopathy System — Extraction & Run Guide

This guide explains how to extract the release archive on a new laptop and run the project.

1) Transfer and extract
- Copy `diabetic_retinopathy_system_release.zip` to the target laptop and extract to a folder of your choice.

2) Create and activate Python virtual environment
Windows (PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate.ps1   # or use venv\Scripts\activate.bat in cmd.exe
```

Linux / macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

3) Install dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4) Create `.env` from template

```bash
# Linux/macOS
cp .env.example .env
# Windows
copy .env.example .env
```

Edit `.env` to set your database credentials and `SECRET_KEY`. For local testing you can use SQLite by adjusting `settings.py` or adding appropriate environment variables.

5) Apply database migrations

```bash
python manage.py migrate
```

6) Collect static files

```bash
python manage.py collectstatic --noinput
```

7) Create superuser (optional)

```bash
python manage.py createsuperuser
```

8) Run the development server

```bash
python manage.py runserver 0.0.0.0:8000
```

9) Access the app
- Open `http://127.0.0.1:8000/` in your browser.
- For patient progress charts visit `/tracking/progress/<patient_id>/`.

Notes & important info
- The release archive intentionally excludes `venv/`, `.git/`, `media/` and `staticfiles/` to keep the bundle small. If you need uploaded images (media) copy the `media/retina_images/` folder separately.
- If your target machine does not have MySQL, you can configure `settings.py` to use SQLite for quick local tests.
- There are helper scripts in the repo:
  - `setup.bat` (Windows) — sets up venv, installs requirements, runs migrations.
  - `setup.sh` (Linux/macOS) — same as above.
  - `package_project.bat` / `package_project.sh` — create the release zip (run on the source machine before transfer).
  - `diagnostic.py` — run after setup to validate system health: `python diagnostic.py`.

Troubleshooting
- If `Chart.js` is not rendering, run `python manage.py collectstatic --noinput` and hard-refresh the browser (Ctrl+F5).
- If detections appear identical, use `python diagnostic.py` to verify the DB and API responses.

If you want, I can also add a single `release_build.py` script that automates the packaging and optionally includes selected `media/` files.
