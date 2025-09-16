# API Endpoints Documentation

This document lists all available API endpoints for the eCommerce Django project, including the fields for each model and example requests for testing.

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
  - Update: `PUT /api/v1/categories/{id}/`
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

## Example JWT Auth Request
```bash
curl -X POST http://localhost:8000/api/v1/auth/jwt/create/ \
  -H "Content-Type: application/json" \
  -d '{"email": "your_email@example.com", "password": "your_password"}'
```

## Notes
- All endpoints require JWT authentication except registration and login.
- Admin users have full access (CRUD). Regular users have read-only access.
- Use `/api/v1/` as the base path for all endpoints.
