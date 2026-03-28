#!/bin/bash
# Setup script for Linux/macOS
# This script initializes the Diabetic Retinopathy System for a fresh installation

echo ""
echo "============================================"
echo "Diabetic Retinopathy System - Setup"
echo "============================================"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi

python3 --version
echo "✓ Python detected"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 is not installed"
    exit 1
fi

echo "✓ pip detected"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt --quiet
if [ $? -ne 0 ]; then
    echo "ERROR: Failed to install dependencies"
    exit 1
fi
echo "✓ Dependencies installed"

# Create .env file if it doesn't exist
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created - IMPORTANT: Edit .env with your database credentials"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Creating media and staticfiles directories..."
mkdir -p media/retina_images/original
mkdir -p media/retina_images/processed
echo "✓ Directories created"

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py migrate
if [ $? -ne 0 ]; then
    echo "ERROR: Database migrations failed"
    echo "Make sure your database is running and credentials in .env are correct"
    exit 1
fi
echo "✓ Database migrations completed"

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput
if [ $? -ne 0 ]; then
    echo "WARNING: Failed to collect static files (non-critical)"
fi
echo "✓ Static files collected"

# Create superuser (optional)
echo ""
echo ""
read -p "Do you want to create a superuser account now? (y/n): " create_user
if [[ "$create_user" == "y" || "$create_user" == "Y" ]]; then
    python manage.py createsuperuser
fi

# Display next steps
echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "Next Steps:"
echo "1. Edit .env file with your database credentials if needed"
echo "2. Start the development server:"
echo "   python manage.py runserver"
echo ""
echo "3. Access the application at:"
echo "   http://127.0.0.1:8000/"
echo ""
echo "4. Login with the superuser account you created"
echo ""
echo "============================================"
echo ""
