@echo off
title Django E-Commerce Project - Full Setup & Run
color 0A

echo =======)
echo.

REM Handle migrations for fresh setup
echo 🗄️ Checking database setup...
if exist "db.sqlite3" (
    echo ✅ Database file exists. Checking for conflicts...
) else (
    echo 📝 No database file found. This appears to be a fresh setup.
)

REM Check if this is a fresh clone (migrations exist but no database)
if exist "store\migrations\0001_initial.py" (
    if not exist "db.sqlite3" (
        echo 🔄 Fresh project detected! Existing migrations found but no database.
        echo 💡 For a clean setup, we'll reset migrations...
        set /p reset_migrations="Reset migrations for fresh setup? (recommended for new clones) (y/n): "
        if /i "%reset_migrations%"=="y" (
            echo 🧹 Cleaning existing migrations...
            del /q store\migrations\*.py 2>nul
            echo # Django migrations > store\migrations\__init__.py
            echo ✅ Migrations cleaned for fresh setup.
        )
    )
)

REM Create database migrations
echo 🔄 Creating database migrations...
python manage.py makemigrations store
if %errorlevel% neq 0 (
    echo ❌ Failed to create migrations!
    echo 🔧 Check your models.py and settings.py configuration.
    echo 💡 If you're getting conflicts, try deleting migration files manually.
    pause
    exit /b 1
)=========================================
echo 🚀 Django E-Commerce Project - Complete Setup Script
echo ============================================================
echo 📅 Welcome! This script will set up everything for you.
echo 💡 Perfect for new clones or fresh project setup.
echo ============================================================
echo.

REM Check if Python is installed
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo 📝 Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
echo ✅ Python is installed and available.
echo.

REM Check if MySQL/WAMP is running
echo 🔍 Checking MySQL connection...
python -c "import mysql.connector; mysql.connector.connect(host='localhost', user='root', password='')" >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ MySQL connection failed!
    echo 🔧 Please ensure WAMP/MySQL is running:
    echo    1. Start WAMP server (wait for green icon)
    echo    2. Make sure MySQL service is running
    echo    3. Verify 'ecommerce' database exists
    echo    4. Test connection in MySQL Workbench
    echo.
    set /p continue="Continue anyway? (not recommended) (y/n): "
    if /i not "%continue%"=="y" (
        echo 🛑 Setup cancelled. Please start MySQL and try again.
        echo 💡 This project requires MySQL database to function properly.
        pause
        exit /b 1
    )
    echo ⚠️  Continuing without MySQL verification...
) else (
    echo ✅ MySQL connection successful.
)
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ❌ Failed to create virtual environment!
        pause
        exit /b 1
    )
    echo ✅ Virtual environment created successfully.
) else (
    echo ✅ Virtual environment already exists.
)
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat

if not defined VIRTUAL_ENV (
    echo ❌ Failed to activate virtual environment!
    echo 🔧 Try running this script as administrator.
    pause
    exit /b 1
)
echo ✅ Virtual environment activated: %VIRTUAL_ENV%
echo.

REM Check if requirements.txt exists and install dependencies
if exist "requirements.txt" (
    echo 📋 Installing Python dependencies...
    echo � This may take a few minutes for first-time setup...
    pip install --upgrade pip
    pip install -r requirements.txt
    if %errorlevel% neq 0 (
        echo ❌ Failed to install dependencies!
        echo 🔧 Check your internet connection and try again.
        pause
        exit /b 1
    )
    echo ✅ All dependencies installed successfully.
) else (
    echo ⚠️  requirements.txt not found. Skipping dependency installation.
)
echo.

REM Create database migrations
echo 🔄 Creating database migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ❌ Failed to create migrations!
    echo � Check your models.py and settings.py configuration.
    pause
    exit /b 1
)
echo ✅ Database migrations created.
echo.

REM Apply migrations
echo 📦 Applying database migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Failed to apply migrations!
    echo 🔧 Check your database connection and try again.
    pause
    exit /b 1
)
echo ✅ Database migrations applied successfully.
echo.

REM Check if superuser exists, offer to create one
echo 👤 Checking for admin user...
python -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0 if User.objects.filter(is_superuser=True).exists() else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo 📝 No admin user found.
    set /p create_admin="Would you like to create an admin user? (y/n): "
    if /i "%create_admin%"=="y" (
        echo 🔐 Creating admin user...
        python manage.py createsuperuser
        if %errorlevel% neq 0 (
            echo ⚠️  Admin user creation was cancelled or failed.
        ) else (
            echo ✅ Admin user created successfully.
        )
    )
) else (
    echo ✅ Admin user already exists.
)
echo.

REM Collect static files
echo 🎨 Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ⚠️  Static files collection failed, but continuing...
) else (
    echo ✅ Static files collected successfully.
)
echo.

REM Generate fake data
echo 🎲 Generating sample data...
python manage.py generate_fake_data
if %errorlevel% neq 0 (
    echo ⚠️  Sample data generation failed, but continuing...
    echo 💡 You can generate sample data later with: python manage.py generate_fake_data
) else (
    echo ✅ Sample data generated successfully.
)
echo.

REM Display project information
echo ============================================================
echo 🎉 SETUP COMPLETE! Your Django project is ready to go!
echo ============================================================
echo.
echo 🌐 API Endpoints will be available at:
echo    • Main API: http://127.0.0.1:8000/store/
echo    • Admin Panel: http://127.0.0.1:8000/admin/
echo    • Products: http://127.0.0.1:8000/store/products/
echo    • Categories: http://127.0.0.1:8000/store/categories/
echo    • Orders: http://127.0.0.1:8000/store/orders/
echo.
echo � Development Commands:
echo    • Stop server: Ctrl+C
echo    • Restart: run this script again
echo    • Manual start: python manage.py runserver
echo.
echo 📚 Project Features:
echo    • ✅ Product Management
echo    • ✅ Order Processing  
echo    • ✅ Payment Handling
echo    • ✅ User Profiles
echo    • ✅ Category Management
echo    • ✅ Sample Data Generated
echo.
echo ============================================================

REM Start development server
echo �🚀 Starting Django development server...
echo 💡 Press Ctrl+C to stop the server when you're done.
echo.
python manage.py runserver

REM Server stopped
echo.
echo ============================================================
echo 👋 Django development server stopped.
echo 🔄 Run this script again anytime to restart the project!
echo ============================================================
pause
