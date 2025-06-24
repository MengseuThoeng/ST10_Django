@echo off
echo Activating virtual environment...

call venv\Scripts\activate.bat

if not defined VIRTUAL_ENV (
    echo ❌ Failed to activate virtual environment.
    exit /b 1
)

echo ✅ Virtual environment activated.

echo 🔄 Running makemigrations...
python manage.py makemigrations

echo 📦 Running migrate...
python manage.py migrate

echo 🎒 Mockup data files...
python manage.py generate_fake_data

echo 🚀 Starting development server...
python manage.py runserver
