@echo off
title MySQL Connection Diagnostic Tool
color 0E

echo ============================================================
echo 🔍 MySQL Connection Diagnostic Tool
echo ============================================================
echo This tool will help diagnose MySQL connection issues.
echo ============================================================
echo.

echo 1️⃣ Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed or not in PATH!
    pause
    exit /b 1
)
python --version
echo ✅ Python is available.
echo.

echo 2️⃣ Activating virtual environment (if exists)...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo ✅ Virtual environment activated.
) else (
    echo ⚠️ No virtual environment found. Using system Python.
)
echo.

echo 3️⃣ Checking mysql-connector-python installation...
python -c "import mysql.connector; print('mysql-connector-python version:', mysql.connector.__version__)" 2>nul
if %errorlevel% neq 0 (
    echo ❌ mysql-connector-python is not installed!
    echo 💡 Installing it now...
    pip install mysql-connector-python
    if %errorlevel% neq 0 (
        echo ❌ Failed to install mysql-connector-python!
        pause
        exit /b 1
    )
    echo ✅ mysql-connector-python installed successfully.
) else (
    echo ✅ mysql-connector-python is installed.
)
echo.

echo 4️⃣ Testing MySQL connection with detailed output...
python -c "
import mysql.connector
import sys

print('🔍 Attempting to connect to MySQL...')
print('Connection details:')
print('  Host: localhost')
print('  Port: 3306')
print('  User: root')
print('  Password: (empty)')
print()

try:
    # Test connection
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        port=3306,
        connection_timeout=10
    )
    
    print('✅ Successfully connected to MySQL!')
    
    # Get MySQL version
    cursor = conn.cursor()
    cursor.execute('SELECT VERSION()')
    version = cursor.fetchone()
    print(f'📊 MySQL Version: {version[0]}')
    
    # List databases
    cursor.execute('SHOW DATABASES')
    databases = cursor.fetchall()
    print(f'🗄️ Available databases:')
    for db in databases:
        print(f'   • {db[0]}')
    
    # Check if ecommerce database exists
    cursor.execute('SHOW DATABASES LIKE \"ecommerce\"')
    ecommerce_exists = cursor.fetchone()
    if ecommerce_exists:
        print('✅ ecommerce database exists')
        
        # Check tables in ecommerce
        cursor.execute('USE ecommerce')
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        if tables:
            print(f'📋 Tables in ecommerce database:')
            for table in tables:
                print(f'   • {table[0]}')
        else:
            print('📝 ecommerce database is empty (no tables)')
    else:
        print('⚠️ ecommerce database does not exist')
    
    cursor.close()
    conn.close()
    print()
    print('🎉 MySQL connection test completed successfully!')
    
except mysql.connector.Error as e:
    print(f'❌ MySQL Error: {e}')
    print()
    print('🔧 Possible solutions:')
    print('   • Make sure WAMP Server is running (green icon)')
    print('   • Check if MySQL service is started in WAMP')
    print('   • Verify MySQL is running on port 3306')
    print('   • Try restarting WAMP services')
    print('   • Check Windows Services for MySQL service')
    sys.exit(1)
    
except Exception as e:
    print(f'❌ Connection Error: {e}')
    print()
    print('🔧 Possible solutions:')
    print('   • Check if WAMP Server is installed and running')
    print('   • Verify firewall is not blocking port 3306')
    print('   • Try connecting with MySQL Workbench first')
    print('   • Check WAMP logs for errors')
    sys.exit(1)
"

if %errorlevel% neq 0 (
    echo.
    echo ============================================================
    echo 🛠️ TROUBLESHOOTING GUIDE
    echo ============================================================
    echo.
    echo 📋 Step-by-step MySQL setup:
    echo.
    echo 1. Install WAMP Server:
    echo    • Download from: https://www.wampserver.com/
    echo    • Install with default settings
    echo.
    echo 2. Start WAMP:
    echo    • Click WAMP icon in system tray
    echo    • Wait for icon to turn GREEN (not orange/red)
    echo    • This may take a few minutes
    echo.
    echo 3. Check MySQL Service:
    echo    • Left-click WAMP icon
    echo    • Go to MySQL ^> Service administration
    echo    • Ensure service is "Started"
    echo.
    echo 4. Test with MySQL Workbench:
    echo    • Open MySQL Workbench
    echo    • Connect to localhost:3306
    echo    • User: root, Password: (leave empty)
    echo.
    echo 5. Check Windows Services:
    echo    • Press Win+R, type "services.msc"
    echo    • Look for "wampmysqld64" or similar
    echo    • Make sure it's "Running"
    echo.
    echo 💡 Common issues:
    echo    • Port 3306 blocked by firewall
    echo    • Another MySQL instance running
    echo    • WAMP not fully started (orange icon)
    echo    • Missing Visual C++ Redistributables
    echo.
    pause
) else (
    echo.
    echo ============================================================
    echo 🎉 MySQL is working perfectly!
    echo ============================================================
    echo You can now run fresh_setup.bat or run_project.bat
    echo ============================================================
    pause
)
