# Ecommerce Practice Project --- Overview

## 1. Project Summary

**Project name:** Ecommerce\
**Project type:** Small e-commerce web application\
**Purpose:** Practice Python, Django, Django ORM, MySQL, authentication,
CRUD operations, and basic order/payment workflows.

This is a learning project. The first version should stay small and
understandable. Build the features step by step and avoid unnecessary
complexity.

## 2. Technology Stack

-   **Backend:** Python 3.12, Django
-   **Database:** MySQL 8.4
-   **Database driver:** `mysqlclient`
-   **Frontend:** Django Templates (HTML), CSS, Bootstrap, and
    JavaScript as needed
-   **Development environment:** VS Code and a project-specific virtual
    environment (`.venv`)

## 3. Project Structure

``` text
Ecommerce/
│
├── .venv/
├── config/              # Project settings and root URL configuration
├── accounts/            # User registration, login, logout, and profiles
├── products/            # Product listing, details, and product CRUD
├── categories/          # Product categories
├── cart/                # Add, update, and remove cart items
├── orders/              # Checkout and order management
├── payments/            # Basic payment workflow / gateway integration practice
├── reviews/             # Product ratings and reviews
├── dashboard/           # Admin-facing management dashboard
│
├── templates/           # Shared project-level templates (if needed)
├── static/              # Shared CSS, JavaScript, and images (if needed)
├── media/               # Uploaded product images
├── .env                 # Local environment variables; never commit this file
├── .gitignore
├── manage.py
└── requirements.txt
```

The app folders listed above are the planned feature modules. The shared
`templates/`, `static/`, `media/`, `.env`, `.gitignore`, and
`requirements.txt` entries are supporting project files/folders, not
additional Django apps.

## 4. Django App Responsibilities

  -----------------------------------------------------------------------
  App                     Main responsibility     Practice features
  ----------------------- ----------------------- -----------------------
  `accounts`              User authentication and Register, login,
                          profile                 logout, profile

  `products`              Product management      Product list, detail
                                                  page,
                                                  create/update/delete
                                                  products

  `categories`            Product categorization  Category list and
                                                  category-based
                                                  filtering

  `cart`                  Shopping cart           Add to cart, change
                                                  quantity, remove item,
                                                  view subtotal

  `orders`                Order processing        Checkout, create order,
                                                  order items, order
                                                  history

  `payments`              Payment workflow        Payment status and a
                                                  sandbox/test payment
                                                  flow

  `reviews`               Customer feedback       Rating, review text,
                                                  and product reviews

  `dashboard`             Management interface    Overview of products,
                                                  orders, and users
  -----------------------------------------------------------------------

For the first practice version, use Django's built-in authentication
system. Do not add a custom user model unless the project requirements
later justify it.

## 5. Main User Roles

### Customer

-   Register and log in.
-   Browse products and categories.
-   View product details.
-   Add products to the cart.
-   Place an order.
-   View their order history.
-   Submit a review for a product they have purchased (optional for the
    first version).

### Administrator / Staff

-   Log in to the Django admin.
-   Manage products and categories.
-   Review and update orders.
-   View basic dashboard information.

## 6. Main Application Flow

1.  A visitor opens the home page.
2.  The visitor browses categories and products.
3.  The visitor opens a product details page.
4.  The customer adds a product to the cart.
5.  The customer reviews the cart and proceeds to checkout.
6.  The system creates an order and its order items.
7.  The payment module records the payment result.
8.  The customer can view the order status in their account.

For practice, begin with a **Cash on Delivery** or mock payment option.
Integrate a real payment gateway only after the order workflow is
working correctly.

## 7. Initial Database Model Plan

The following is a planning guide, not final model code. Fields and
relationships should be finalized while implementing each app.

-   **Category:** category name, slug, description, active status
-   **Product:** category, name, slug, description, price, stock
    quantity, image, active status
-   **Cart / Cart Item:** customer or session reference, product,
    quantity
-   **Order:** customer, order number, total amount, status, shipping
    details, created date
-   **Order Item:** order, product reference, product name/price
    snapshot, quantity, line total
-   **Payment:** order, payment method, amount, transaction reference
    (if applicable), status
-   **Review:** customer, product, rating, comment, created date

Use `DecimalField` for money values rather than floating-point fields.
Define foreign keys and deletion behavior carefully. Store an order-item
price snapshot so later product price changes do not alter old orders.

## 8. Suggested Development Phases

### Phase 1 --- Project Foundation

-   Create the Django project using the `config` package.
-   Create the listed Django apps.
-   Add each app to `INSTALLED_APPS`.
-   Confirm Django connects to the MySQL database.
-   Configure shared templates, static files, and media files.

### Phase 2 --- Categories and Products

-   Create category and product models.
-   Register them in Django admin.
-   Run migrations.
-   Add product and category CRUD pages.
-   Display product images.

### Phase 3 --- Accounts

-   Implement registration, login, logout, and profile pages.
-   Protect customer-only pages.

### Phase 4 --- Cart

-   Add products to the cart.
-   Update quantities and remove items.
-   Calculate subtotals and cart total.
-   Validate stock on the server side.

### Phase 5 --- Orders and Checkout

-   Collect shipping details.
-   Create orders and order items inside a database transaction.
-   Recheck stock during checkout.
-   Update stock only when the order is successfully placed.

### Phase 6 --- Payments

-   Start with Cash on Delivery or a mock payment.
-   Record payment status.
-   Add a real gateway only when the rest of the checkout flow is
    stable.

### Phase 7 --- Reviews and Dashboard

-   Add product ratings and reviews.
-   Build a simple staff dashboard.
-   Add basic order and product summaries.

### Phase 8 --- Testing and Cleanup

-   Test models, forms, views, and permissions.
-   Test invalid inputs and stock edge cases.
-   Check that customers cannot access other customers' orders.
-   Keep secrets in `.env`.
-   Add dependencies to `requirements.txt`.

## 9. Basic Security and Quality Rules

-   Never commit `.env` or expose database passwords and Django secret
    keys.
-   Use Django's password hashing and authentication features.
-   Keep CSRF protection enabled for forms.
-   Validate all important data on the server side.
-   Check object ownership and permissions before showing or changing
    customer data.
-   Do not trust prices or totals sent by the browser; calculate them on
    the server.
-   Use database transactions for checkout and stock updates.
-   Do not store raw card details.
-   Use a payment gateway's sandbox environment when practising gateway
    integration.
-   Keep `DEBUG = True` only for local development.

## 10. Definition of Done --- First Practice Version

The first version is complete when a customer can:

-   Register and log in.
-   Browse categories and products.
-   Add products to a cart and update quantities.
-   Complete a basic checkout.
-   Create an order and view its status.

An administrator can manage products, categories, and orders through
Django admin.

**Scope note:** Keep the first version small. Build and test one app at
a time. Payment gateway integration, advanced dashboards, coupons,
shipping integrations, and complex inventory features can wait until the
core shopping flow works.
