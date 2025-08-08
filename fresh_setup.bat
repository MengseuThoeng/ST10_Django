@echo off
title Django E-Commerce - Fresh Setup (New Users)
color 0B

echo ============================================================
echo 🆕 Django E-Commerce - FRESH SETUP SCRIPT
echo ============================================================
echo 👋 Welcome! This script is for COMPLETELY NEW setups.
echo 🎯 Use this if you just cloned the project or want a clean start.
echo ============================================================
echo.

echo ⚠️  WARNING: This will reset ALL database and migration data!
echo 📝 This script will:
echo    • Delete existing database (db.sqlite3)
echo    • Clean all migration files
echo    • Create fresh virtual environment
echo    • Install all dependencies
echo    • Create new database from scratch
echo    • Generate sample data
echo.
set /p confirm="Are you sure you want to proceed? (y/n): "
if /i not "%confirm%"=="y" (
    echo 🛑 Setup cancelled.
    pause
    exit /b 0
)
echo.

echo ============================================================
echo 🧹 CLEANING EXISTING DATA
echo ============================================================

REM Remove existing database
if exist "db.sqlite3" (
    echo 🗑️ Removing existing database...
    del db.sqlite3
    echo ✅ Database removed.
) else (
    echo 💡 No existing database found.
)

REM Clean migrations
echo 🧹 Cleaning migration files...
if exist "store\migrations" (
    del /q store\migrations\*.py 2>nul
    echo # Django migrations > store\migrations\__init__.py
    echo ✅ Migration files cleaned.
) else (
    mkdir store\migrations
    echo # Django migrations > store\migrations\__init__.py
    echo ✅ Migrations directory created.
)

REM Remove existing virtual environment
if exist "venv" (
    echo 📦 Removing existing virtual environment...
    rmdir /s /q venv
    echo ✅ Old virtual environment removed.
)

REM Clean Python cache
if exist "__pycache__" (
    echo 🧹 Cleaning Python cache...
    rmdir /s /q __pycache__ 2>nul
)
if exist "store\__pycache__" (
    rmdir /s /q store\__pycache__ 2>nul
)
if exist "eCommerce\__pycache__" (
    rmdir /s /q eCommerce\__pycache__ 2>nul
)
echo ✅ Python cache cleaned.
echo.

echo ============================================================
echo 🔧 FRESH ENVIRONMENT SETUP
echo ============================================================

REM Check Python installation
echo 🔍 Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    echo 📝 Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)
python --version
echo ✅ Python is ready.
echo.

REM Create fresh virtual environment
echo 📦 Creating fresh virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ Failed to create virtual environment!
    pause
    exit /b 1
)
echo ✅ Virtual environment created.
echo.

REM Activate virtual environment
echo 🔄 Activating virtual environment...
call venv\Scripts\activate.bat
if not defined VIRTUAL_ENV (
    echo ❌ Failed to activate virtual environment!
    pause
    exit /b 1
)
echo ✅ Virtual environment activated.
echo.

REM Install dependencies
echo 📋 Installing fresh dependencies...
echo 💾 This will take a few minutes...
pip install --upgrade pip
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies!
    pause
    exit /b 1
)
echo ✅ All dependencies installed.
echo.

echo ============================================================
echo 🗄️ MYSQL DATABASE SETUP
echo ============================================================

echo ⚠️  IMPORTANT: MySQL Setup Required!
echo.
echo 🔧 Before continuing, please ensure:
echo    ✅ WAMP Server is running (GREEN icon)
echo    ✅ MySQL service is started
echo    ✅ You can access phpMyAdmin or MySQL Workbench
echo.
echo 💡 Quick WAMP startup:
echo    1. Click WAMP icon in system tray
echo    2. Wait for icon to turn GREEN
echo    3. Left-click WAMP → MySQL → Service administration → Start Service
echo.
set /p ready="WAMP/MySQL is ready and running? (y/n): "
if /i not "%ready%"=="y" (
    echo.
    echo 🛑 Please start WAMP/MySQL first, then run this script again.
    echo 📋 Need help? Check SETUP_GUIDE.md for detailed instructions.
    pause
    exit /b 1
)
echo ✅ Great! Proceeding with setup...
echo.

echo 🗄️ Database Setup Instructions:
echo.
echo ⚠️  PLEASE CREATE 'ecommerce' DATABASE MANUALLY:
echo    1. Open phpMyAdmin (http://localhost/phpmyadmin)
echo    2. OR open MySQL Workbench
echo    3. Create database: CREATE DATABASE ecommerce;
echo    4. Make sure it's empty (no tables)
echo.
echo 💡 Why manual setup?
echo    • Ensures you have proper MySQL access
echo    • Avoids connection issues during setup
echo    • Gives you control over database creation
echo.
set /p db_ready="Have you created the 'ecommerce' database? (y/n): "
if /i not "%db_ready%"=="y" (
    echo.
    echo 🛑 Please create the 'ecommerce' database first.
    echo 📋 Steps:
    echo    1. Open phpMyAdmin: http://localhost/phpmyadmin
    echo    2. Click "New" on the left side
    echo    3. Database name: ecommerce
    echo    4. Click "Create"
    echo    5. Then run this script again
    pause
    exit /b 1
)
echo ✅ Great! Database is ready. Continuing with migrations...
echo.

REM Create fresh migrations
echo 🔄 Creating fresh database migrations...
python manage.py makemigrations store
if %errorlevel% neq 0 (
    echo ❌ Failed to create migrations!
    pause
    exit /b 1
)
echo ✅ Fresh migrations created.
echo.

REM Apply migrations
echo 📦 Setting up database schema...
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ Failed to apply migrations!
    pause
    exit /b 1
)
echo ✅ Database schema created.
echo.

REM Create superuser
echo 👤 Creating admin user...
echo 📝 You'll need this to access the admin panel.
python manage.py createsuperuser
if %errorlevel% neq 0 (
    echo ⚠️  Superuser creation was cancelled or failed.
    echo 💡 You can create one later with: python manage.py createsuperuser
) else (
    echo ✅ Admin user created successfully.
)
echo.

REM Collect static files
echo 🎨 Collecting static files...
python manage.py collectstatic --noinput
if %errorlevel% neq 0 (
    echo ⚠️  Static files collection failed.
) else (
    echo ✅ Static files collected.
)
echo.

REM Generate sample data
echo 🎲 Generating sample data...
python manage.py generate_fake_data
if %errorlevel% neq 0 (
    echo ⚠️  Sample data generation failed.
    echo 💡 You can generate it later with: python manage.py generate_fake_data
) else (
    echo ✅ Sample data generated successfully.
)
echo.

echo ============================================================
echo 🎉 FRESH SETUP COMPLETE!
echo ============================================================
echo.
echo 🌟 Your Django E-Commerce project is now ready!
echo.
echo 🌐 Access your application:
echo    • API Base: http://127.0.0.1:8000/store/
echo    • Admin Panel: http://127.0.0.1:8000/admin/
echo    • Products API: http://127.0.0.1:8000/store/products/
echo    • Categories API: http://127.0.0.1:8000/store/categories/
echo    • Orders API: http://127.0.0.1:8000/store/orders/
echo.
echo 📚 What's been set up:
echo    ✅ Fresh virtual environment
echo    ✅ All dependencies installed
echo    ✅ Clean MySQL database with schema
echo    ✅ Admin user account
echo    ✅ Sample data for testing
echo    ✅ Static files collected
echo.
echo 🚀 Next steps:
echo    1. Run: python manage.py runserver
echo    2. Or use: run_project.bat for future runs
echo    3. Visit http://127.0.0.1:8000/admin/ to manage data
echo    4. Test API endpoints with Postman or browser
echo.
echo 💡 Quick commands for development:
echo    • Start server: python manage.py runserver
echo    • Create migrations: python manage.py makemigrations
echo    • Apply migrations: python manage.py migrate
echo    • Create superuser: python manage.py createsuperuser
echo    • Generate test data: python manage.py generate_fake_data
echo.
echo ============================================================

set /p start_server="Start the development server now? (y/n): "
if /i "%start_server%"=="y" (
    echo.
    echo 🚀 Starting Django development server...
    echo 💡 Press Ctrl+C to stop the server.
    echo.
    python manage.py runserver
    echo.
    echo 👋 Server stopped.
)

echo.
echo 🎯 Setup complete! You can now start developing.
echo 🔄 For future runs, just use: run_project.bat
echo ============================================================
pause
