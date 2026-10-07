# ⚡ ApexStore - Modern E-Commerce Platform

A feature-complete, modern full-stack e-commerce web application built with **Django (Python)** on the backend and **HTML5, CSS3, and Vanilla JavaScript** on the frontend, with an **SQLite** database for storing products, users, carts, and orders.

---

## 🌟 Key Features

1. **Product Catalog & Browsing**:
   - Clean, responsive card grid with responsive image scaling and hover animations.
   - Category filtering (Electronics, Fashion, Home & Living, Fitness & Sports) with active pills.
   - Real-time search by product name, description, or category.
   - Sorting options: Featured, Price (Low to High / High to Low), Customer Rating, and Newest.
   - Stock indicators ("In Stock" count, "Sold Out" state).

2. **Product Details Page**:
   - Detailed product view with high-res photography, star ratings, and review counts.
   - Quantity selector (+ / - controls).
   - Instant "Add to Cart" with asynchronous toast notification.
   - "Buy Now" one-click shortcut straight to checkout.
   - Related products carousel/grid.

3. **Dynamic Shopping Cart**:
   - Asynchronous (AJAX) item quantity increase/decrease without full page reload.
   - Instant item removal with animation.
   - Live recalculation of Subtotal, Shipping (Free above $100 threshold), Tax (8%), and Grand Total.
   - Dynamic navbar cart badge counter automatically synchronized across the application.
   - Session-based guest carts automatically merge into user account carts upon login.

4. **Order Processing & Checkout**:
   - Comprehensive checkout form capturing full shipping address and contact details.
   - Payment method selector: Credit/Debit Card (Demo), Cash on Delivery (COD), PayPal (Demo).
   - Atomic database transactions: creates `Order` with unique Order ID, records individual `OrderItem` rows, deducts inventory `stock` in real-time, and clears the cart.
   - Order Confirmation receipt page with printable summary and delivery tracking.

5. **User Authentication & Dashboard**:
   - User Registration with form validation and password strength enforcement.
   - User Login and Logout with session security.
   - "My Orders" customer dashboard listing past purchases, dates, itemized breakdowns, total spent, and status badges (`Pending`, `Processing`, `Shipped`, `Delivered`).

6. **Admin Dashboard**:
   - Django Admin (`/admin/`) configured for inventory management, product addition, order fulfillment, and category organization.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.14, Django 6.1
- **Database**: SQLite (relational, zero configuration required)
- **Frontend**: HTML5 semantic markup, Custom CSS3 Design System (CSS variables, Flexbox, Grid), Vanilla JavaScript (ES6+ Fetch API for AJAX cart operations)
- **Authentication**: Django Auth Framework (PBKDF2 SHA-256 password hashing)

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+ (Python 3.14 is installed in this workspace)

### 2. Activate the Virtual Environment
From the project directory:

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```
*(Or run commands directly using `.\venv\Scripts\python.exe`)*

### 3. Run Migrations & Seed Data (Already Prepared)
```powershell
.\venv\Scripts\python manage.py migrate
.\venv\Scripts\python manage.py seed_products
```

### 4. Start the Development Server
```powershell
.\venv\Scripts\python manage.py runserver
```
Visit the store in your browser at: **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 🔑 Demo Credentials

| Role | Username | Password | Email |
| :--- | :--- | :--- | :--- |
| **Admin** | `admin` | `adminpassword123` | `admin@example.com` |
| **Customer** | `demouser` | `demopassword123` | `demo@example.com` |

- **Admin Dashboard**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
- **Customer Sign In**: [http://127.0.0.1:8000/accounts/login/](http://127.0.0.1:8000/accounts/login/)

---

## 🧪 Running Automated Tests

Run the test suite covering catalog, cart, user registration/login, and checkout processing:

```powershell
.\venv\Scripts\python manage.py test
```

---

## 📁 Project Structure

```
E-commerce/
├── manage.py                          # Django management CLI
├── requirements.txt                   # Project dependencies
├── db.sqlite3                         # SQLite database
├── ecommerce_store/                   # Main project configuration
│   ├── settings.py                    # Settings, apps, templates, static config
│   ├── urls.py                        # Root URL routing
│   └── wsgi.py                        # WSGI server entry point
├── store/                             # Catalog and Cart Application
│   ├── models.py                      # Category, Product, Cart, CartItem
│   ├── views.py                       # Product listings, details, AJAX cart actions
│   ├── urls.py                        # Store endpoints
│   ├── admin.py                       # Admin panel models
│   ├── cart_utils.py                  # Session/user cart helpers & merger
│   ├── context_processors.py          # Global categories and cart counter
│   ├── tests.py                       # Catalog and cart test cases
│   └── management/commands/seed_products.py # Sample data generator
├── accounts/                          # User Authentication Application
│   ├── forms.py                       # User registration and login forms
│   ├── views.py                       # Register, login, logout, order history
│   ├── urls.py                        # Auth routes
│   └── tests.py                       # Auth test cases
├── orders/                            # Order Processing Application
│   ├── models.py                      # Order, OrderItem
│   ├── forms.py                       # Checkout shipping form
│   ├── views.py                       # Checkout, order_success, order_detail
│   ├── urls.py                        # Order routes
│   ├── admin.py                       # Order management in admin
│   └── tests.py                       # Order processing test cases
├── templates/                         # HTML Templates
│   ├── base.html                      # Header, navigation, footer, alerts
│   ├── store/
│   │   ├── product_list.html          # Catalog, search, filtering, hero banner
│   │   ├── product_detail.html        # Single product view, quantity, buy now
│   │   └── cart.html                  # Full cart management & order summary
│   ├── orders/
│   │   ├── checkout.html              # Shipping details & payment choice
│   │   ├── order_success.html         # Receipt & order confirmation
│   │   └── order_detail.html          # Individual order details
│   └── accounts/
│       ├── login.html                 # Login card
│       ├── register.html              # Registration card
│       └── orders_history.html        # Customer orders dashboard
└── static/                            # Static Assets
    ├── css/
    │   └── style.css                  # Custom responsive design system
    ├── js/
    │   └── main.js                    # AJAX cart handler, toasts, DOM events
    └── images/
        └── placeholder.svg            # Fallback SVG placeholder
```
