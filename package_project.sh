#!/usr/bin/env bash
# Package project into a portable zip (Linux/macOS)
set -e
ZIPNAME=diabetic_retinopathy_system_release.zip
echo "Creating $ZIPNAME in parent directory..."
zip -r ../$ZIPNAME . -x "venv/*" ".git/*" "media/*" "staticfiles/*" "__pycache__/*" "*.pyc" ".env" "venv/*"
echo "Created ../$ZIPNAME"
