# Diabetic Retinopathy Detection System - Complete Setup & Deployment Guide

## Quick Start (5 minutes)

### Windows
```bash
# 1. Extract the project folder
# 2. Open Command Prompt in the project folder
# 3. Run setup
setup.bat

# 4. Start the server
python manage.py runserver
```

### Linux / macOS
```bash
# 1. Extract the project folder
# 2. Open Terminal in the project folder
# 3. Make setup script executable
chmod +x setup.sh

# 4. Run setup
./setup.sh

# 5. Start the server
python manage.py runserver
```

### Access the Application
- **URL:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **Default Login:** Use the superuser account created during setup

---

## Prerequisites

### System Requirements
- **Python:** 3.8 or higher
- **MySQL/MariaDB:** 5.7 or higher
- **RAM:** Minimum 2GB (4GB recommended)
- **Disk Space:** Minimum 500MB

### Software to Install
1. **Python 3.8+** - https://www.python.org/downloads/
2. **MySQL Server** - https://dev.mysql.com/downloads/mysql/
   - Or **MariaDB** - https://mariadb.org/download/
3. **Git** (optional) - https://git-scm.com/

---

## Detailed Setup Instructions

### Step 1: Database Setup

#### Windows - MySQL
```batch
# Start MySQL service
net start MySQL80

# Or open MySQL Command Line Client and create database
CREATE DATABASE retinopathy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'retino_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON retinopathy_db.* TO 'retino_user'@'localhost';
FLUSH PRIVILEGES;
```

#### Linux - MySQL
```bash
sudo mysql -u root -p
CREATE DATABASE retinopathy_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'retino_user'@'localhost' IDENTIFIED BY 'secure_password';
GRANT ALL PRIVILEGES ON retinopathy_db.* TO 'retino_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 2: Project Setup

```bash
# Extract the project
# Navigate to project folder
cd diabetic_retinopathy_system

# Copy environment template
cp .env.example .env        # Linux/macOS
copy .env.example .env      # Windows

# Edit .env with your database credentials
# DB_USER=retino_user
# DB_PASSWORD=secure_password
# DB_NAME=retinopathy_db
```

### Step 3: Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

#### Linux/macOS
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Step 4: Database Migrations

```bash
python manage.py migrate
```

### Step 5: Create Superuser

```bash
python manage.py createsuperuser

# Follow prompts:
# Username: admin
# Email: admin@example.com
# Password: (create a strong password)
```

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 7: Start Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

---

## Configuration Files

### .env File (Required)
Located in project root. Edit with your settings:

```ini
# Security
SECRET_KEY=your-secret-key-change-in-production
DEBUG=True  # Set to False in production

# Database
DB_ENGINE=django.db.backends.mysql
DB_NAME=retinopathy_db
DB_USER=root
DB_PASSWORD=Root
DB_HOST=localhost
DB_PORT=3306

# Allowed hosts (comma-separated)
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
```

### settings.py
Already configured to read from .env file. Key settings:
- **Database:** MySQL backend
- **Static files:** `static/` and `staticfiles/`
- **Media files:** `media/`
- **Installed apps:** All custom apps included
- **Templates:** Bootstrap5 styling configured

---

## Directory Structure

```
diabetic_retinopathy_system/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Template for environment variables
├── setup.bat                # Setup script for Windows
├── setup.sh                 # Setup script for Linux/macOS
├── diagnostic.py            # Diagnostic and testing script
│
├── retinopathy_system/       # Main Django project
│   ├── settings.py          # Configuration
│   ├── urls.py              # URL routing
│   ├── wsgi.py              # WSGI for production
│   └── asgi.py              # ASGI for async
│
├── users/                   # User management app
├── images/                  # Retina image upload/management
├── detection/               # Microaneurysm detection
├── tracking/                # Patient progress tracking
├── reports/                 # Report generation
├── custom_admin/            # Admin customization
├── dashboard/               # Dashboard views
│
├── templates/               # HTML templates
├── static/                  # CSS, JS, images
├── media/                   # Uploaded files
│   └── retina_images/
│       ├── original/        # Original uploads
│       └── processed/       # Detection results
│
└── migrations/              # Database migrations (auto-generated)
```

---

## Key Features

### 1. Image Upload & Management
- Upload retina fundus images
- Support for JPEG, PNG formats
- Automatic image validation

### 2. Microaneurysm Detection
- OpenCV-based detection
- Confidence score calculation
- Automatic lesion area calculation
- Processing time tracking

### 3. Patient Progress Tracking
- Track multiple detections per patient
- Visual charts with Chart.js:
  - **Microaneurysms Over Time** (Line chart)
  - **Lesion Area Over Time** (Line chart)
  - **Confidence Score Trend** (Line chart)
  - **Detection Comparison** (Bar chart)
- Detection history table with timestamps

### 4. Report Generation
- PDF report generation
- Detailed detection analysis
- Progress summaries

---

## Troubleshooting

### Issue: "No module named 'django'"
```bash
# Ensure virtual environment is activated
# Windows:
venv\Scripts\activate

# Linux/macOS:
source venv/bin/activate

# Then reinstall:
pip install -r requirements.txt
```

### Issue: "MySQL connection error"
```bash
# Check MySQL is running
# Windows:
net start MySQL80

# Linux:
sudo service mysql status
sudo service mysql start

# Verify .env credentials:
cat .env  # Linux/macOS
type .env # Windows
```

### Issue: "No migrations available"
```bash
python manage.py makemigrations
python manage.py migrate
```

### Issue: "Charts not displaying"
```bash
# Collect static files
python manage.py collectstatic --noinput

# Clear browser cache (Ctrl+Shift+Delete) and reload
# Verify data exists:
python diagnostic.py
```

### Issue: "All detections show same values (99.00%)"
```bash
# Run diagnostic to check data variance
python diagnostic.py

# If data is correct but not displaying:
# 1. Hard refresh browser (Ctrl+F5)
# 2. Check browser console for JavaScript errors
# 3. Restart dev server

# If data itself is same:
# Upload more images and run multiple detections
```

---

## Testing & Verification

### Run Diagnostic Report
```bash
python diagnostic.py
```

This checks:
- ✓ Database connection
- ✓ Detection data variety
- ✓ API response format
- ✓ Template configuration
- ✓ Static files

### Create Test Data
```bash
# Create sample detections for testing
python manage.py shell

from detection.models import DetectionResult
from images.models import RetinaImage

# Script to generate test data if needed
```

---

## Production Deployment

### Pre-Production Checklist

```bash
# 1. Update settings for production
DEBUG=False

# 2. Generate secure secret key
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# 3. Set in .env:
SECRET_KEY=<generated-key>
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# 4. Run security checks
python manage.py check --deploy

# 5. Collect static files
python manage.py collectstatic --noinput

# 6. Create backup of database
# mysqldump -u root -p retinopathy_db > backup.sql
```

### Deployment Options

#### Option 1: Gunicorn + Nginx (Recommended)
```bash
# Install gunicorn
pip install gunicorn

# Run with gunicorn
gunicorn retinopathy_system.wsgi:application --bind 0.0.0.0:8000

# Configure Nginx as reverse proxy (separate guide)
```

#### Option 2: Apache + mod_wsgi
- Configure Apache with mod_wsgi
- Point to `retinopathy_system/wsgi.py`

#### Option 3: Docker
```bash
# Build image
docker build -t retinopathy-system .

# Run container
docker run -p 8000:8000 retinopathy-system
```

---

## Data Backup & Recovery

### Backup Database
```bash
# MySQL backup
mysqldump -u root -p retinopathy_db > backup_$(date +%Y%m%d).sql

# Backup media files
tar -czf media_backup_$(date +%Y%m%d).tar.gz media/
```

### Restore Database
```bash
mysql -u root -p retinopathy_db < backup_20260129.sql
```

---

## Performance Optimization

### Database Optimization
```bash
# Create indexes on frequently queried fields
python manage.py shell
from django.db import connection
connection.cursor().execute("""
    CREATE INDEX idx_patient_status ON detection_detectionresult(status);
    CREATE INDEX idx_detection_date ON detection_detectionresult(detection_date);
""")
```

### Static Files
- Use CDN for static files in production
- Enable gzip compression
- Use whitenoise for serving static files

### Caching
- Enable Django cache framework
- Use Redis for session storage
- Implement template fragment caching

---

## Support & Documentation

### Additional Resources
- Django Docs: https://docs.djangoproject.com/
- OpenCV Guide: https://docs.opencv.org/
- Chart.js Docs: https://www.chartjs.org/docs/latest/

### Common Commands

```bash
# Start development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run diagnostic
python diagnostic.py
```

---

## Security Recommendations

1. **Change default password** immediately after setup
2. **Use strong SECRET_KEY** in production
3. **Enable HTTPS/SSL** in production
4. **Set DEBUG=False** in production
5. **Use environment variables** for sensitive data
6. **Regular database backups**
7. **Keep dependencies updated:** `pip install --upgrade -r requirements.txt`
8. **Implement user authentication** properly
9. **Validate all user inputs**
10. **Use CSRF protection** (enabled by default)

---

## License & Usage

This system is designed for medical research and clinical use. Ensure compliance with:
- Local medical data privacy regulations (HIPAA, GDPR, etc.)
- Medical device regulations if used in clinical setting
- Institutional review boards (IRB) approval if conducting research

---

**Last Updated:** January 29, 2026
**Version:** 1.0
