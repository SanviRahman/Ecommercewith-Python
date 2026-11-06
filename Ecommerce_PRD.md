# Product Requirements Document (PRD)

## Ecommerce Practice Project

**Document version:** 1.0\
**Project name:** Ecommerce\
**Project type:** Small practice e-commerce application\
**Status:** Initial product requirements

------------------------------------------------------------------------

## 1. Product Overview

### 1.1 Purpose

Build a small e-commerce web application to practise Python, Django,
Django ORM, MySQL, authentication, CRUD operations, and a basic shopping
and order workflow.

The first release should remain small, understandable, and modular.
Development will proceed one Django app at a time.

### 1.2 Technology

-   **Backend:** Python 3.12, Django
-   **Database:** MySQL 8.4
-   **Database driver:** `mysqlclient`
-   **Frontend:** Django Templates, HTML, CSS, Bootstrap, and JavaScript
    as needed
-   **Development:** VS Code and a project-specific `.venv`

### 1.3 Product Goals

1.  Let visitors browse products and categories.
2.  Let customers register, sign in, manage a cart, and place a basic
    order.
3.  Let staff manage catalogue data and orders.
4.  Provide an admin Trash where supported records can be soft-deleted,
    restored, or permanently deleted with safeguards.
5.  Practise Django models, relationships, forms, views, permissions,
    migrations, and testing using MySQL.

------------------------------------------------------------------------

## 2. Users and Roles

### 2.1 Visitor

-   Browse active products and categories.
-   View product details.
-   Register or sign in.

### 2.2 Customer

-   Register, log in, log out, and manage a basic profile.
-   Browse active products and categories.
-   Add products to the cart, change quantities, and remove cart items.
-   Complete a basic checkout.
-   View their own order history and order status.
-   Submit a product review, where enabled.

### 2.3 Staff / Administrator

-   Access the protected administration area.
-   Create, view, update, and manage products and categories.
-   Review and update orders.
-   Manage reviews.
-   View a basic dashboard summary.
-   Move supported records to Trash and restore them.

### 2.4 Superuser

-   Has all staff capabilities.
-   Can permanently delete eligible records after an explicit
    confirmation.
-   Can manage staff access and permissions.

------------------------------------------------------------------------

## 3. Django Application Structure

The implementation should follow the app structure in the project
overview.

``` text
Ecommerce/
│
├── config/              # Project settings and root URLs
├── accounts/            # Registration, login, logout, profiles
├── products/            # Product catalogue and product CRUD
├── categories/          # Product categories
├── cart/                # Shopping cart
├── orders/              # Checkout and order management
├── payments/            # Payment method and payment status
├── reviews/             # Product ratings and reviews
├── dashboard/           # Admin-facing dashboard and management entry points
│
├── templates/           # Shared templates, if needed
├── static/              # CSS, JavaScript, and static images
├── media/               # Uploaded product images
├── .env                 # Local secrets; never commit
├── .gitignore
├── requirements.txt
└── manage.py
```

Do not create additional Django apps unless implementation reveals a
clear need. Shared reusable code may be placed in an appropriate
existing project module without changing the app structure
unnecessarily.

------------------------------------------------------------------------

## 4. Functional Requirements

Priority labels: - **Must:** Required for the first usable version. -
**Should:** Valuable, but can follow the core workflow. - **Could:**
Optional practice enhancement.

### 4.1 Accounts

-   **ACC-01 --- Must:** A visitor can register with valid account
    details.
-   **ACC-02 --- Must:** A customer can log in and log out.
-   **ACC-03 --- Must:** Customer-only pages require authentication.
-   **ACC-04 --- Should:** A customer can view and update basic profile
    information.
-   **ACC-05 --- Must:** Use Django's built-in authentication system for
    the first version; do not introduce a custom user model without a
    later requirement.
-   **ACC-06 --- Must:** Staff-only administration functions must check
    staff permissions.

### 4.2 Categories

-   **CAT-01 --- Must:** Staff can create, view, and update categories.
-   **CAT-02 --- Must:** Visitors can browse active categories.
-   **CAT-03 --- Must:** Visitors can filter active products by an
    active category.
-   **CAT-04 --- Must:** Categories support the soft-delete lifecycle
    described in Section 5.
-   **CAT-05 --- Must:** A category with linked products cannot be
    permanently deleted until those product relationships are safely
    resolved.

### 4.3 Products

-   **PROD-01 --- Must:** Staff can create, view, and update products.
-   **PROD-02 --- Must:** A product contains at least a name, category,
    description, price, stock quantity, active status, and optional
    image.
-   **PROD-03 --- Must:** Visitors can browse active products and view
    product details.
-   **PROD-04 --- Must:** Products in Trash must not appear in public
    catalogue, search, category results, or cart additions.
-   **PROD-05 --- Must:** Product price uses a decimal database field,
    not floating-point storage.
-   **PROD-06 --- Must:** Stock and price are validated on the server;
    browser-submitted totals are not trusted.
-   **PROD-07 --- Must:** Products support the soft-delete lifecycle
    described in Section 5.
-   **PROD-08 --- Must:** A product referenced by historical order items
    cannot be permanently deleted until the order-history relationship
    is safely resolved. Preserve order-item name and price snapshots.

### 4.4 Cart

-   **CART-01 --- Must:** A customer can add an active product to the
    cart.
-   **CART-02 --- Must:** A customer can change item quantity and remove
    an item.
-   **CART-03 --- Must:** The cart displays line subtotals and a total
    calculated on the server.
-   **CART-04 --- Must:** The system validates available stock before
    checkout.
-   **CART-05 --- Must:** A product in Trash or inactive cannot be newly
    added to a cart or checked out.
-   **CART-06 --- Must:** Removing a cart item is a normal cart
    operation, not a Trash operation.

### 4.5 Orders and Checkout

-   **ORD-01 --- Must:** An authenticated customer can submit shipping
    details and place an order.
-   **ORD-02 --- Must:** The system creates an order and its order
    items.
-   **ORD-03 --- Must:** Order creation and stock updates use a database
    transaction.
-   **ORD-04 --- Must:** Stock is rechecked during checkout to avoid
    selling unavailable stock.
-   **ORD-05 --- Must:** Order items preserve product-name and
    unit-price snapshots.
-   **ORD-06 --- Must:** A customer can view only their own orders.
-   **ORD-07 --- Must:** Staff can review orders and update allowed
    order statuses.
-   **ORD-08 --- Must:** Orders are not permanently deleted through the
    normal admin Trash workflow. Use order status changes such as
    cancelled/refunded where appropriate, preserving the transaction
    history.

### 4.6 Payments

-   **PAY-01 --- Must:** The first version supports Cash on Delivery or
    a mock/test payment workflow.
-   **PAY-02 --- Must:** The system records payment method, amount, and
    payment status.
-   **PAY-03 --- Must:** Raw card numbers, CVV values, or other
    sensitive card credentials are never stored.
-   **PAY-04 --- Must:** Payment records are retained and are not
    permanently deleted through the normal Trash workflow.
-   **PAY-05 --- Should:** A real payment gateway may be added later
    using its sandbox environment.

### 4.7 Reviews

-   **REV-01 --- Should:** A customer can submit a rating and review for
    a product.
-   **REV-02 --- Should:** Staff can view and moderate reviews.
-   **REV-03 --- Must:** Reviews support soft delete, restore, and
    permanent deletion with the rules in Section 5.
-   **REV-04 --- Must:** Trashed reviews are not shown publicly.

### 4.8 Dashboard and Administration

-   **ADM-01 --- Must:** The first release uses Django's built-in Admin
    as the primary management interface.
-   **ADM-02 --- Must:** Staff can manage products, categories, reviews,
    and orders according to permissions.
-   **ADM-03 --- Should:** The `dashboard` app provides a simple
    overview of products, orders, and users.
-   **ADM-04 --- Must:** The admin interface provides access to Trash
    for supported soft-deletable records.
-   **ADM-05 --- Must:** Admin actions clearly distinguish **Move to
    Trash**, **Restore**, and **Permanently Delete**.
-   **ADM-06 --- Must:** Bulk actions are available for moving eligible
    selected records to Trash and restoring selected records.
-   **ADM-07 --- Must:** Permanent deletion requires a separate
    confirmation step and is restricted to superusers.
-   **ADM-08 --- Must:** Admin operations must enforce server-side
    permissions; hiding a button alone is not sufficient.
-   **ADM-09 --- Should:** Admin logs should record who performed a
    Trash, Restore, or Permanent Delete action where practical.

------------------------------------------------------------------------

## 5. Soft Delete, Trash, Restore, and Permanent Delete

### 5.1 Purpose

The admin panel must provide a recoverable deletion workflow for
catalogue and review content. A normal delete action must not
immediately remove supported records from the database.

### 5.2 Records Covered by Soft Delete

The first version applies soft delete to:

-   **Category**
-   **Product**
-   **Review**

The following records are intentionally handled differently to protect
business history:

-   **Order and Payment:** Do not expose permanent deletion in the
    normal Trash workflow. Preserve these records; use status changes
    such as cancelled, refunded, or inactive where appropriate.
-   **User accounts:** Deactivate accounts using Django's account status
    (`is_active`) rather than permanently deleting them through Trash.
-   **Cart items:** Remove cart items normally; they are temporary
    shopping data.

### 5.3 Soft Delete Data

Each soft-deletable model must track:

-   `is_deleted` --- Boolean flag; default `False`.
-   `deleted_at` --- Nullable timestamp set when the record is moved to
    Trash.
-   `deleted_by` --- Nullable reference to the staff user who moved it
    to Trash.

Use a reusable abstract model or equivalent shared implementation so the
behavior remains consistent across Category, Product, and Review.

### 5.4 Record States

A supported record has one of two states:

1.  **Active:** `is_deleted = False`; available in normal admin lists
    and, if otherwise active, eligible for public display.
2.  **Trashed:** `is_deleted = True`; hidden from public pages and
    normal active admin lists, but visible in Trash to authorized staff.

### 5.5 Move to Trash

-   **TRASH-01:** Staff with the required permission can move a
    supported record to Trash.
-   **TRASH-02:** Moving a record to Trash sets `is_deleted = True`,
    records `deleted_at`, and records `deleted_by`.
-   **TRASH-03:** The database row is retained; this operation must not
    call a physical database delete.
-   **TRASH-04:** The record immediately disappears from public
    catalogue/review results and normal active admin lists.
-   **TRASH-05:** The admin receives a clear success message.
-   **TRASH-06:** Bulk move-to-Trash is supported for eligible selected
    records.

### 5.6 Trash View

-   **TRASH-07:** Admin users with permission can open a Trash view.
-   **TRASH-08:** Trash can be filtered by record type: Categories,
    Products, and Reviews.
-   **TRASH-09:** Each row displays useful context, including record
    name/title, deletion date, and deleted-by user where available.
-   **TRASH-10:** Trash provides Restore and Permanently Delete actions
    according to permissions.
-   **TRASH-11:** Trashed records must not be accidentally included in
    normal product/category/review querysets.

### 5.7 Restore

-   **RESTORE-01:** Authorized staff can restore a trashed record.
-   **RESTORE-02:** Restore sets `is_deleted = False`,
    `deleted_at = NULL`, and `deleted_by = NULL`.
-   **RESTORE-03:** A restored record returns to normal admin lists.
-   **RESTORE-04:** A restored product/category/review becomes publicly
    eligible only if its other active/status rules are satisfied.
-   **RESTORE-05:** Bulk restore is supported for eligible selected
    records.
-   **RESTORE-06:** Restore must validate relationships and uniqueness
    constraints. If restoration would create a conflict (for example, a
    duplicate unique slug), show a clear error and do not partially
    restore the record.

### 5.8 Permanent Delete

-   **DELETE-01:** Permanent deletion physically removes a record from
    the database and is irreversible through the application.
-   **DELETE-02:** Only a superuser can permanently delete records in
    the first version.
-   **DELETE-03:** Permanent deletion is available only from Trash, not
    as the default delete action in active lists.
-   **DELETE-04:** The system must show a confirmation page/message
    naming the record and warning that the action cannot be undone.
-   **DELETE-05:** The operation must respect database relationships and
    constraints.
-   **DELETE-06:** A category with linked products cannot be permanently
    deleted until products are reassigned or the relationship is
    otherwise safely resolved.
-   **DELETE-07:** A product referenced by order history cannot be
    permanently deleted while doing so would damage historical order
    data.
-   **DELETE-08:** Orders and payments are excluded from permanent
    deletion in the normal admin UI.
-   **DELETE-09:** If permanent deletion is blocked by a relationship or
    constraint, show a clear explanation and leave the record unchanged.
-   **DELETE-10:** Bulk permanent delete may be offered only to
    superusers and must use a confirmation step listing/counting the
    selected records.

### 5.9 Query and Visibility Rules

-   Normal application queries must return only non-deleted records by
    default.
-   Admin active lists must not silently mix active and trashed records.
-   Trash queries must explicitly return deleted records.
-   Public product/category/review pages must exclude trashed records.
-   Cart and checkout must reject trashed or inactive products.
-   Soft deletion of a category must not cascade-delete its products.
    Products in a trashed category should not be publicly discoverable
    until the category is restored or the product is assigned to another
    active category.
-   Soft deletion must not delete order, payment, or order-item history.

------------------------------------------------------------------------

## 6. Initial Data Model Guidance

This is a requirements-level model plan; finalize fields and
relationships during implementation.

  -----------------------------------------------------------------------
  Model                               Main data
  ----------------------------------- -----------------------------------
  Category                            Name, slug, description, active
                                      status, soft-delete fields

  Product                             Category, name, slug, description,
                                      price, stock, image, active status,
                                      soft-delete fields

  Cart / Cart Item                    Customer or session reference,
                                      product, quantity

  Order                               Customer, order number, total,
                                      status, shipping details, created
                                      date

  Order Item                          Order, product reference where
                                      appropriate, product-name and price
                                      snapshots, quantity, line total

  Payment                             Order, method, amount, transaction
                                      reference if applicable, status

  Review                              Customer, product, rating, comment,
                                      created date, soft-delete fields
  -----------------------------------------------------------------------

### Data integrity rules

-   Use a decimal field for money.
-   Use database foreign keys and appropriate deletion behavior.
-   Preserve order-item product-name and price snapshots.
-   Do not cascade-delete orders or payments when a product is moved to
    Trash.
-   Use transactions for checkout, stock changes, and multi-record
    operations where needed.

------------------------------------------------------------------------

## 7. Non-Functional Requirements

-   **Security:** Keep secrets in `.env`; never commit `.env`.
-   **Authentication:** Use Django's authentication and password
    hashing.
-   **Authorization:** Enforce staff/superuser permissions on every
    admin action.
-   **CSRF:** Keep CSRF protection enabled for forms and state-changing
    requests.
-   **Validation:** Validate user input and business rules on the
    server.
-   **Data integrity:** Use transactions for checkout and stock updates.
-   **Maintainability:** Keep apps focused on their responsibilities and
    avoid unnecessary abstractions.
-   **Usability:** Show clear success/error messages for admin actions.
-   **Development safety:** Keep `DEBUG = True` only for local
    development.
-   **Testing:** Cover models, views, permissions, soft delete, restore,
    and permanent delete.

------------------------------------------------------------------------

## 8. Acceptance Criteria

The first release is acceptable when the following can be demonstrated.

### Core shopping workflow

-   [ ] A visitor can browse active categories and products.
-   [ ] A customer can register, log in, and log out.
-   [ ] A customer can add an active product to the cart.
-   [ ] A customer can update quantity and remove cart items.
-   [ ] The system calculates totals on the server.
-   [ ] A customer can place a basic order.
-   [ ] A customer can view only their own order history.
-   [ ] Staff can manage products, categories, and orders.

### Soft-delete workflow

-   [ ] Staff can move a product to Trash.
-   [ ] A trashed product disappears from public catalogue and
    cart/checkout.
-   [ ] Staff can view the product in Trash.
-   [ ] Authorized staff can restore the product.
-   [ ] A restored product returns to active admin lists and is publicly
    eligible if its other status rules allow it.
-   [ ] Staff can move a category and review to Trash.
-   [ ] Trashed categories and reviews are hidden from public pages.
-   [ ] A superuser can permanently delete an eligible trashed record
    after confirmation.
-   [ ] A non-superuser cannot permanently delete records, even by
    directly submitting a crafted request.
-   [ ] A category with linked products cannot be permanently deleted
    without resolving the relationship.
-   [ ] A product used in order history cannot be permanently deleted if
    that would damage order history.
-   [ ] Orders and payments remain preserved.
-   [ ] Bulk Trash and Restore actions work only for authorized users.
-   [ ] Unique-field conflicts are handled safely during restore.

### Technical verification

-   [ ] Django connects to MySQL 8.4.
-   [ ] Migrations apply successfully.
-   [ ] No `.env` secrets are committed.
-   [ ] Tests cover soft delete, restore, permanent delete, and
    permissions.

------------------------------------------------------------------------

## 9. Development Plan

Implement and test one app or feature group at a time.

1.  **Foundation:** Project configuration, MySQL, shared
    templates/static/media, app registration.
2.  **Categories and Products:** Models, admin registration, migrations,
    catalogue pages, image handling, and soft-delete lifecycle.
3.  **Accounts:** Registration, login, logout, profile, and permissions.
4.  **Cart:** Add/update/remove, totals, and stock validation.
5.  **Orders:** Checkout, order items, transactions, and order history.
6.  **Payments:** Cash on Delivery or mock payment and payment status.
7.  **Reviews and Dashboard:** Review moderation, Trash integration, and
    basic management summary.
8.  **Testing and Cleanup:** Permission tests, data-integrity tests,
    regression tests, and `requirements.txt`.

------------------------------------------------------------------------

## 10. Out of Scope for the First Version

-   Live payment processing and storing card details.
-   Advanced shipping-provider integrations.
-   Coupons, loyalty points, and complex promotions.
-   Multi-vendor marketplace functionality.
-   Complex warehouse/inventory management.
-   Permanent deletion of orders or payment records from the admin
    Trash.
-   Advanced analytics and reporting.

These features can be considered after the basic shopping, order, and
soft-delete workflows are stable.

------------------------------------------------------------------------

## 11. Product Success Definition

The practice project is successful when a customer can browse products,
manage a cart, and place a basic order; staff can manage the catalogue
and orders; and authorized administrators can safely move supported
records to Trash, restore them, or permanently delete eligible records
with confirmation and relationship safeguards.
