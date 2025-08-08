# 🚀 Setup Scripts Guide - MySQL E-Commerce Project

This Django E-Commerce project is designed to work with **MySQL database only**. Both setup scripts ensure proper MySQL configuration.

## 📋 Prerequisites

**Required:**
- Python 3.8+
- WAMP Server (Windows) or XAMPP
- MySQL running on localhost:3306
- Root user with no password (default WAMP setup)

## 📁 Available Scripts

### 1. `fresh_setup.bat` - For Brand New Setup
**🎯 Use this when:**
- You just cloned the project for the first time
- You want to completely reset everything
- You're setting up on a new machine
- You're having migration conflicts

**✨ What it does:**
- 🔍 **Verifies MySQL connection** (required)
- 🗄️ **Creates/cleans 'ecommerce' database**
- 🧹 **Removes existing data and migrations**
- 📦 **Creates fresh virtual environment**
- 🔧 **Installs all dependencies**
- 🗄️ **Creates clean database schema**
- 👤 **Sets up admin user account**
- 🎲 **Generates sample data**
- 🚀 **Optional: Starts development server**

**⚡ Quick Start:**
```bash
# Make sure WAMP is running first!
fresh_setup.bat
```

### 2. `run_project.bat` - For Regular Development
**🎯 Use this when:**
- Project is already set up
- You want to start development server
- You need to apply new migrations
- Daily development workflow

**✨ What it does:**
- ✅ **Verifies MySQL connection**
- 🔄 **Activates virtual environment**
- 📋 **Installs any new dependencies**
- 🗄️ **Handles migration conflicts intelligently**
- 🔄 **Applies database migrations**
- 🎲 **Generates fresh sample data**
- 🚀 **Starts development server**

**⚡ Quick Start:**
```bash
# Make sure WAMP is running first!
run_project.bat
```

## 🎯 Which Script Should I Use?

### For New Users/Fresh Clone:
```
1. Run: fresh_setup.bat (first time only)
2. Then use: run_project.bat (for daily development)
```

### For Existing Users:
```
Just run: run_project.bat
```

### For Troubleshooting:
```
If you have issues: fresh_setup.bat (resets everything)
```

## 🛠️ Manual Commands (Alternative)

If you prefer manual setup:

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create migrations
python manage.py makemigrations store

# Apply migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Generate sample data
python manage.py generate_fake_data

# Start server
python manage.py runserver
```

## 🌐 Access Points

After setup, your application will be available at:

- **Main API**: http://127.0.0.1:8000/store/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **API Documentation**: http://127.0.0.1:8000/store/products/
- **Categories**: http://127.0.0.1:8000/store/categories/
- **Orders**: http://127.0.0.1:8000/store/orders/

## 🆘 Troubleshooting

### Common Issues:

**❌ "MySQL connection failed"**
- Start WAMP server and wait for green icon
- Ensure MySQL service is running in WAMP
- Check that MySQL is on localhost:3306
- Verify root user has no password
- Test connection in MySQL Workbench

**❌ "Python not found"**
- Install Python 3.8+ from python.org
- Add Python to system PATH during installation

**❌ "ecommerce database not found"**
- Scripts will create it automatically
- Or manually: `CREATE DATABASE ecommerce;` in MySQL

**❌ "Migration conflicts"**
- Run `fresh_setup.bat` to reset everything
- This will clean all migrations and recreate them

**❌ "Permission denied"**
- Run script as Administrator
- Check antivirus software blocking Python

**❌ "Virtual environment failed"**
- Ensure you have write permissions in project folder
- Try running as Administrator

### MySQL Setup Steps:

1. **Install WAMP Server**
   - Download from wampserver.com
   - Install with default settings

2. **Start WAMP**
   - Click WAMP icon in system tray
   - Wait for icon to turn green

3. **Verify MySQL**
   - Open MySQL Workbench
   - Connect to localhost:3306
   - User: root, Password: (empty)

4. **Run Setup Script**
   - Execute `fresh_setup.bat`
   - Script will create 'ecommerce' database automatically

## 💡 Development Workflow

```
Day 1: fresh_setup.bat
Day 2+: run_project.bat
```

## 🔧 Advanced Options

### Environment Variables (Optional):
```bash
# MySQL Configuration (default values)
set DB_ENGINE=mysql
set DB_NAME=ecommerce
set DB_USER=root
set DB_PASSWORD=
set DB_HOST=localhost
set DB_PORT=3306
```

### Custom Settings:
Edit `eCommerce/settings.py` for advanced MySQL configuration.

### Database Management:
```bash
# Access MySQL command line
mysql -u root -p

# Basic database commands
SHOW DATABASES;
USE ecommerce;
SHOW TABLES;
DESCRIBE table_name;
```

---

**Happy coding! 🎉**
