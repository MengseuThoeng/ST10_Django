# 🛒 Django Store Project

A basic Django project with a product store page and MySQL database.

---

## ⚙️ Project Automation + MySQL Cleanup (Windows Only)

### 1️⃣ Create Virtual Environment

    python -m venv venv

---

### 2️⃣ Activate venv & Install Dependencies

    venv\Scripts\activate
    pip install -r requirements.txt

---

### 3️⃣ Open WAMP & MySQL Workbench

- 🚀 Start WAMP (click the WAMP icon)
- 🧠 Open MySQL Workbench

---

### 4️⃣ Clean `ecommerce` Database (Drop All Tables)

In MySQL Workbench, run:

    USE ecommerce;

    SET FOREIGN_KEY_CHECKS = 0;

    SET @tables = NULL;
    SELECT GROUP_CONCAT('`', table_name, '`') INTO @tables
    FROM information_schema.tables
    WHERE table_schema = 'ecommerce';

    SET @tables = IFNULL(@tables, 'dummy');
    SET @del_stmt = CONCAT('DROP TABLE IF EXISTS ', @tables);
    PREPARE stmt FROM @del_stmt;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;

    SET FOREIGN_KEY_CHECKS = 1;

✅ This removes all tables in the `ecommerce` database.

---

### 5️⃣ Run the Project Automatically

Just run:

    run_project.bat

This will:
- ✅ Activate venv
- 🔄 Run makemigrations
- 📦 Run migrate
- 🎒 Collect static files
- 🚀 Start the dev server

---

### 🌐 Access the API

- http://127.0.0.1:8000/store/
---

### ✅ Done!

Your Django project is live — let's build bro! 💻🔥
