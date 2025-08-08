# 🛒 Django E-Commerce Store API

A comprehensive Django REST API for an e-commerce platform with product management, order processing, payment handling, and user profiles. Built with Django REST Framework and MySQL database.

## 🚀 Features

- **Product Management**: CRUD operations for products with categories
- **Order System**: Order processing with status tracking (Pending, Completed, Cancelled)
- **Payment Processing**: Payment management with multiple methods support
- **User Profiles**: Extended user information with address and contact details
- **Category Management**: Product categorization with many-to-many relationships
- **Nested API Routes**: Category-specific products and order payments
- **Fake Data Generation**: Built-in command for generating test data

## 🛠️ Tech Stack

- **Backend**: Django 5.1.7 + Django REST Framework 3.16.0
- **Database**: MySQL with mysqlclient
- **API**: RESTful API with nested routing support
- **Testing**: Faker for generating test data

## 📋 Prerequisites

- Python 3.8+
- MySQL Server (WAMP recommended for Windows)
- MySQL Workbench (optional but recommended)

## 🔧 Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone <your-repo-url>
cd DjangoProject
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
```

### 3️⃣ Activate Virtual Environment & Install Dependencies
```bash
# Windows
venv\Scripts\activate

# Install requirements
pip install -r requirements.txt
```

### 4️⃣ Database Setup

#### Start WAMP Server
- 🚀 Start WAMP (click the WAMP icon)
- 🧠 Open MySQL Workbench

#### Clean Database (if needed)
In MySQL Workbench, run:
```sql
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
```

### 5️⃣ Quick Start (Automated)

Run the automated setup script:
```bash
run_project.bat
```

This script automatically:
- ✅ Activates virtual environment
- 🔄 Creates database migrations
- 📦 Applies migrations to database
- 🎒 Collects static files
- 🚀 Starts development server

## 🌐 API Endpoints

Base URL: `http://127.0.0.1:8000/store/`

### Products
- `GET /store/products/` - List all products
- `POST /store/products/` - Create new product
- `GET /store/products/{id}/` - Get specific product
- `PUT /store/products/{id}/` - Update product
- `DELETE /store/products/{id}/` - Delete product

### Categories
- `GET /store/categories/` - List all categories
- `POST /store/categories/` - Create new category
- `GET /store/categories/{id}/` - Get specific category
- `PUT /store/categories/{id}/` - Update category
- `DELETE /store/categories/{id}/` - Delete category

### Category Products (Nested)
- `GET /store/categories/{category_id}/products/` - Get products in category

### Orders
- `GET /store/orders/` - List all orders
- `POST /store/orders/` - Create new order
- `GET /store/orders/{id}/` - Get specific order
- `PUT /store/orders/{id}/` - Update order
- `DELETE /store/orders/{id}/` - Delete order

### Payments (Nested under Orders)
- `GET /store/orders/{order_id}/payments/` - Get payments for order
- `POST /store/orders/{order_id}/payments/` - Create payment for order

## 🗄️ Database Models

### UserProfile
- Extended user information with address, phone, city, state, zipcode

### Products
- Product details with name, price, quantity, categories, and soft delete

### Category
- Product categories with many-to-many relationship to products

### Orders
- Order management with status tracking and product relationships

### Payment
- Payment processing with multiple methods and order relationships

## 🎲 Generate Test Data

Use the built-in management command to generate fake data:
```bash
python manage.py generate_fake_data
```

## 🖥️ Manual Setup (Alternative)

If you prefer manual setup:

```bash
# Activate virtual environment
venv\Scripts\activate

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run development server
python manage.py runserver
```

## � Project Structure

```
DjangoProject/
├── eCommerce/          # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/              # Main application
│   ├── models.py       # Database models
│   ├── views.py        # API views
│   ├── serializers.py  # DRF serializers
│   ├── routes.py       # URL patterns
│   ├── admin.py        # Admin interface
│   └── management/     # Custom commands
│       └── commands/
│           └── generate_fake_data.py
├── templates/          # HTML templates
├── static/            # Static files
├── requirements.txt   # Python dependencies
└── run_project.bat    # Automated setup script
```

## 🔑 Key Features Explained

### Nested Routing
The API supports nested resources:
- Products within categories: `/store/categories/{id}/products/`
- Payments within orders: `/store/orders/{id}/payments/`

### Status Management
Orders support three statuses: Pending, Completed, Cancelled

### Soft Delete
Products use soft delete functionality with `is_delete` field

### Payment Methods
Support for multiple payment methods (Credit Card, Cash, ABA Pay, etc.)

## 🧪 Testing

The project includes a Faker-based data generation system for testing:
- Generates realistic product, category, and order data
- Useful for development and testing scenarios

## 📝 Notes

- This project is configured for Windows development with WAMP
- MySQL is the primary database backend
- Django REST Framework provides comprehensive API functionality
- The project includes automated setup for quick development start

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

**Happy coding! 💻🔥**
