# 🛋️ FurniShop – Online Furniture Store

FurniShop is a full-featured **online furniture store** built with **Django** and **Django REST Framework**. The project
includes product catalogues, user registration, shopping cart, order management, and **asynchronous background tasks** (
email notifications and automatic status updates) using Celery. It also comes with **media files, static files, and
pre-populated database** for immediate testing.

---

## 🏆 Project Goals

* Implement a **complete e-commerce backend** for a furniture store.
* Provide **REST API endpoints** for products, categories, cart, and orders.
* Support **custom user registration** and profile management.
* Allow **shopping cart management** (add/remove items, calculate totals).
* Enable **order management** with statuses and automatic transitions.
* Integrate **Celery** for asynchronous tasks: sending confirmation emails and updating order status.
* Fully configured **Django Admin** with search, filters, and inline relationships.

---

## 📦 Technologies & Versions

| Component             | Version |
|-----------------------|---------|
| Python                | 3.13.5  |
| Django                | 5.2.7   |
| Django REST Framework | 3.16.1  |
| Celery                | 5.5.3   |
| Redis                 | 7.0.1   |
| django-celery-beat    | 2.8.1   |
| python-dotenv         | 1.2.1   |
| Pillow                | 12.0.0  |
| django-filter         | 25.2    |

All dependencies are included in `requirements.txt` and can be installed using:

```bash
pip install -r requirements.txt
```

---

## 🗂️ Models Overview

### 1️⃣ Category

* **Fields:** `name`, `slug`, `description`, `image`, `is_active`, `created_at`
* **Required categories:** Chair, Sofa, Table, Wardrobe, Bed, Cabinet/Nightstand, Shelf, Armchair, Outdoor Furniture
* **Admin:** search by name, filter by `is_active`, auto-generate slug

### 2️⃣ Product

* **Fields:** `name`, `slug`, `category` (FK), `description`, `price`, `stock`, `is_available`, `featured`,
  `created_at`, `updated_at`
* **Attributes (choices):** `color`, `material`
* **Images:** 1 required + optional additional images
* **Admin:** search by name, filter by category/color/material, edit price/stock in list view

### 3️⃣ CustomUser

* **Fields:** `first_name`, `last_name`, `phone`, `address`, `birth_date`
* **Methods:** `get_full_name()`
* **Admin:** search by phone/name, filter by address

### 4️⃣ Cart & CartItem

* **Cart:** `user` (OneToOne FK), `updated_at`
* **CartItem:** `cart` (FK), `product` (FK), `quantity`
* **Methods:** `get_total_price()`, `get_total_items()`, `get_total_items_count()`
* **Admin:** filter by user, inline CartItem in cart detail

### 5️⃣ Order & OrderItem

* **Order:** `user`, `order_number`, `status` (pending/processing/shipped/delivered/cancelled), `total_amount`,
  `shipping_address`, `phone`, `notes`, `created_at`, `updated_at`
* **OrderItem:** `order` (FK), `product` (FK), `quantity`, `price` (static at purchase)
* **Admin:** search by order number/user, filter by status/date, inline OrderItem in order detail

---

## 🌐 REST API Endpoints

### Categories

* `GET /api/categories/` — List all categories
* `GET /api/categories/<id>/` — Retrieve a single category

### Products

* `GET /api/products/` — List all products
* `GET /api/products/<id>/` — Retrieve a single product
* Filtering: `?color=white&material=wood&category=table`
* Ordering: `?ordering=-price`

### User

* `POST /api/register/` — Registration
* `POST /api/login/` — Login (session-based)
* `GET /api/profile/` — Retrieve authenticated user profile
* Password change endpoint (advanced)

### Cart

* `GET /api/cart/` — Retrieve current user’s cart
* `POST /api/cart/add/` — Add product to cart
* `POST /api/cart/remove/` — Remove product from cart

### Order

* `GET /api/orders/` — List all orders for authenticated user
* `GET /api/orders/<id>/` — Retrieve a specific order
* `POST /api/orders/create/` — Create new order

---

## 🔧 Celery Integration

### Tasks

1. `send_order_confirmation_email` — Sends an email after order creation
2. `update_order_status` — Automatically changes status from *Pending* → *Processing* after 1 minute

### Run Celery Worker

```bash
celery -A furnishop worker --loglevel=info
```

### Run Celery Beat Scheduler

```bash
celery -A furnishop beat --loglevel=info
```

> Ensure Redis is running at `redis://localhost:6379/0`.

---

## 💻 Installation & Setup

### 1. Clone the repository:

```bash
git clone https://github.com/TAMUNA-CHKOIDZE/furniture-shop.git
cd furniture-shop
```

### 2. Create a virtual environment and activate it:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

### 3. Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file with email credentials:

```env
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
DEFAULT_FROM_EMAIL=your_email@gmail.com
```

### 5. Apply migrations:

```bash
python manage.py migrate
```

### 6. Create superuser for admin:

```bash
python manage.py createsuperuser
```

### 7. Collect static files:

```bash
python manage.py collectstatic
```

---

## 🐳 Docker Setup (Optional)

If the user wants to run the project with Docker:

1. **Build Docker image**:

```bash
docker build -t furnishop .
```

2. **Run Docker container**:

```bash
docker run -d -p 8000:8000 --name furnishop furnishop
```

3. Access the app at [http://localhost:8000](http://localhost:8000)

> Docker setup includes Python, dependencies, and database preloaded. For Celery, make sure Redis container is running.

---

## 🗂 Project Structure

```
furniture-shop/
├── furnishop/            # Django project
├── users/                # CustomUser app
├── categories/           # Category app
├── products/             # Product app
├── cart/                 # Shopping cart
├── orders/               # Orders
├── media/                # Uploaded images
├── static/               # Static assets
├── db.sqlite3            # Pre-populated database (included)
├── requirements.txt
└── README.md
```

---

## 📌 Important Notes

* **Database, media, and static files** are included for evaluation.
* Python **3.13.5** is recommended.
* Ensure Redis is running for Celery tasks.
* In production, configure environment variables securely and consider a production-ready server setup.
* Run **migrations** after cloning the project or changing Docker images:

```bash
python manage.py migrate
```

---

## ⚡ Features Summary

* Complete product catalog with images, categories, and filtering
* User registration, login, and profile management
* Shopping cart and checkout flow
* Order creation, automatic status updates, and confirmation emails
* Django admin fully configured with search, filters, and inlines
* REST API with filtering, ordering, and authentication
* Asynchronous background tasks via Celery
* Media and static files included for quick testing
* Optional Docker setup for easy deployment

---

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome. Fork the repo and submit a pull request.


