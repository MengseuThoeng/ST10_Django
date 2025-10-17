# API Endpoints Documentation

This document lists all available API endpoints for the eCommerce Django project, including the fields for each model, example requests, and sample JSON payloads for testing.

---

## Authentication (JWT)

- **Login:** `POST /api/v1/auth/jwt/create/`
  - Fields: `email`, `password`
- **Refresh Token:** `POST /api/v1/auth/jwt/refresh/`
  - Fields: `refresh`
- **Verify Token:** `POST /api/v1/auth/jwt/verify/`
  - Fields: `token`
- **Register:** `POST /api/v1/auth/users/`
  - Fields: `username`, `email`, `password`, `first_name`, `last_name`, `phone`, `address`, `city`, `state`, `zipcode`
- **Get Current User:** `GET /api/v1/users/me/`
  - Returns current user info based on JWT token
  - Requires: Valid JWT token in Authorization header

---

## UserProfile
- **Model:** `UserProfile`
- **Fields:**
  - `id`, `user`, `address`, `phone`, `city`, `state`, `zipcode`, `avatar`
- **Endpoint:** `/api/v1/userprofiles/` *(custom endpoint if implemented, otherwise managed via registration)*

---

## Category
- **Model:** `Category`
- **Fields:**
  - `id`, `name`, `description`, `product_count`, `status`
- **Endpoints:**
  - List: `GET /api/v1/categories/`
  - Detail: `GET /api/v1/categories/{id}/`
  - Create: `POST /api/v1/categories/`

  - Delete: `DELETE /api/v1/categories/{id}/`

---

## Products
- **Model:** `Products`
- **Fields:**
  - `id`, `name`, `price`, `qty`, `is_delete`, `created_date`, `categories`, `order_count`
- **Endpoints:**
  - List: `GET /api/v1/products/`
  - Detail: `GET /api/v1/products/{id}/`
  - Create: `POST /api/v1/products/`
  - Update: `PUT /api/v1/products/{id}/`
  - Delete: `DELETE /api/v1/products/{id}/`
  - List by Category: `GET /api/v1/categories/{category_pk}/products/`

---

## Orders
- **Model:** `Orders`
- **Fields:**
  - `id`, `qty`, `is_deleted`, `product`, `status`
- **Endpoints:**
  - List: `GET /api/v1/orders/`
  - Detail: `GET /api/v1/orders/{id}/`
  - Create: `POST /api/v1/orders/`
  - Update: `PUT /api/v1/orders/{id}/`
  - Delete: `DELETE /api/v1/orders/{id}/`

---

## Payments
- **Model:** `Payment`
- **Fields:**
  - `id`, `order`, `method`, `amount`, `is_paid`, `paid_at`
- **Endpoints:**
  - List: `GET /api/v1/orders/{order_pk}/payments/`
  - Detail: `GET /api/v1/orders/{order_pk}/payments/{id}/`
  - Create: `POST /api/v1/orders/{order_pk}/payments/`
  - Update: `PUT /api/v1/orders/{order_pk}/payments/{id}/`
  - Delete: `DELETE /api/v1/orders/{order_pk}/payments/{id}/`

---

## Posts (User-Specific Data)
- **Model:** `Post`
- **Fields:**
  - `id`, `title`, `content`, `created_by`, `created_by_username`, `created_at`, `updated_at`, `is_published`
- **Endpoints:**
  - List: `GET /api/v1/posts/` (returns only current user's posts, admins see all)
  - Detail: `GET /api/v1/posts/{id}/` (only if owned by user or user is admin)
  - Create: `POST /api/v1/posts/`
  - Update: `PUT /api/v1/posts/{id}/` (only own posts)
  - Delete: `DELETE /api/v1/posts/{id}/` (only own posts)
- **Note:** Users automatically see only their own posts. Admins can see all posts.

---

## Example JWT Auth Request
```bash
curl -X POST http://localhost:8000/api/v1/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@example.com", "password": "your_password"}'
```

## Get Current User Info
```bash
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Notes
- All endpoints require JWT authentication except registration and login.
- Admin users have full access (CRUD). Regular users have read-only access.
- Use `/api/v1/` as the base path for all endpoints.

---

# Example JSON Payloads for Requests

## Register User (POST /api/v1/auth/users/)
```json
{
  "username": "johndoe",
  "email": "john@example.com",
  "password": "yourpassword",
  "first_name": "John",
  "last_name": "Doe",
  "phone": "123456789",
  "address": "123 Main St",
  "city": "Phnom Penh",
  "state": "Phnom Penh",
  "zipcode": "12000"
}
```

## Category
- Create (POST /api/v1/categories/)
```json
{
  "name": "Electronics",
  "description": "Devices and gadgets."
}
```
- Update (PUT /api/v1/categories/1/)
```json
{
  "name": "Electronics & Gadgets",
  "description": "All electronic devices and gadgets."
}
```

## Product
- Create (POST /api/v1/products/)
```json
{
  "name": "Smartphone",
  "price": 299.99,
  "qty": 50,
  "is_delete": false,
  "categories": [1, 2]
}
```
- Update (PUT /api/v1/products/1/)
```json
{
  "name": "Smartphone Pro",
  "price": 399.99,
  "qty": 40,
  "is_delete": false,
  "categories": [1]
}
```

## Order
- Create (POST /api/v1/orders/)
```json
{
  "qty": 2,
  "is_deleted": false,
  "product": 1,
  "status": "Pending"
}
```
- Update (PUT /api/v1/orders/1/)
```json
{
  "qty": 3,
  "is_deleted": false,
  "product": 1,
  "status": "Completed"
}
```

## Payment
- Create (POST /api/v1/orders/{order_pk}/payments/)
```json
{
  "method": "Credit Card",
  "amount": 599.98,
  "is_paid": true,
  "paid_at": "2025-09-16T10:00:00Z"
}
```
- Update (PUT /api/v1/orders/{order_pk}/payments/1/)
```json
{
  "method": "ABA Pay",
  "amount": 599.98,
  "is_paid": true,
  "paid_at": "2025-09-16T12:00:00Z"
}
```

## Post (User-Specific)
- Create (POST /api/v1/posts/)
```json
{
  "title": "My First Post",
  "content": "This is the content of my post.",
  "is_published": true
}
```
- Update (PUT /api/v1/posts/1/)
```json
{
  "title": "Updated Post Title",
  "content": "Updated content for my post.",
  "is_published": true
}
```

