# Product Requirements Document (PRD)

## Ecommerce Practice Project

**Document version:** 2.1\
**Status:** Updated from the project overview, previous PRD/ERD and
supplied reference screenshots.

------------------------------------------------------------------------

## 1. Product Overview

Build a small modular e-commerce application using Python, Django and
MySQL. The first release includes product catalogue, option-wise
pricing, guest and registered checkout, order/payment workflows,
recoverable deletion, admin RBAC, audit logs, site settings, Meta
tracking and a secure cPanel command runner.

### Technology

-   Python 3.12, Django and Django ORM
-   MySQL 8.4, `mysqlclient`
-   Django Templates, HTML, CSS, Bootstrap and JavaScript
-   `python-dotenv`/hosting environment variables
-   `django-role-permissions` for role-based authorization (candidate
    version 3.2.0; compatibility gate required)
-   `django-jazzmin` for Django Admin UI theme (candidate version 3.0.5;
    compatibility gate required)
-   Django built-in `FileField` / `ImageField`; no separate FileField
    package
-   Pillow for image uploads
-   HTTP client for Meta CAPI

Priority labels: **Must** = first release, **Should** = important
follow-up, **Could** = optional enhancement.

## 2. User Roles

### Visitor / Guest Buyer

-   Browse active products/categories.
-   Use a session-based cart.
-   Checkout without registration.
-   Provide contact/shipping details.
-   Track an order using order number plus email/phone verification or a
    secure guest token.

### Registered Customer

-   Register, login, logout and manage a basic profile.
-   Use a customer cart and checkout.
-   View only their own orders.
-   Submit reviews where enabled.
-   Merge eligible guest cart items into their customer cart after
    login.

### Staff / Admin

-   Access protected admin modules according to assigned
    roles/permissions.
-   Manage products, categories, brands, option values, orders and
    reviews.
-   Use eligible bulk actions and view audit records if permitted.

### Superuser

-   Full administrative access.
-   Manage admin accounts and assign/revoke predefined roles;
    role/permission definitions are maintained in `roles.py` and
    synchronized with `sync_roles`.
-   Permanently delete eligible trashed records after confirmation.
-   Run approved System Commands.
-   Cannot bypass FK/data-integrity safeguards protecting
    order/payment/audit history.

## 3. Django Apps

``` text
Ecommerce/
├── config/
├── core/
├── accounts/
├── categories/
├── products/
├── cart/
├── orders/
├── payments/
├── reviews/
├── dashboard/
├── site_settings/
├── tracking/
├── templates/
├── static/
├── media/
├── .env
├── .gitignore
├── requirements.txt
└── manage.py
```

  ---------------------------------------------------------------------
  App                                Responsibility
  ---------------------------------- ----------------------------------
  `config`                           Settings, root URLs, ASGI/WSGI

  `core`                             Abstract SoftDeleteModel, HasSEO,
                                     managers/helpers

  `accounts`                         Built-in authentication, customer
                                     profile and account state

  `categories`                       Category CRUD, visibility and SEO

  `products`                         Product, Brand, options,
                                     option-wise pricing, stock and SEO

  `cart`                             Guest/user carts and selected
                                     option rows

  `orders`                           Guest/registered checkout, orders
                                     and snapshots

  `payments`                         COD/mock payment and status

  `reviews`                          Reviews and moderation

  `dashboard`                        Admins, django-role-permissions
                                     RBAC, audit, bulk actions and
                                     System Commands

  `site_settings`                    Logo, favicon, contact and footer

  `tracking`                         Meta Pixel, CAPI and event logs
  ---------------------------------------------------------------------

Use Django's built-in User model. Admins are users with `is_staff=True`;
custom roles/permissions control custom admin actions.

## 4. Functional Requirements

### 4.1 Accounts and Authentication

-   **ACC-01 --- Must:** Visitor can register with valid details.
-   **ACC-02 --- Must:** Registered customer can login/logout.
-   **ACC-03 --- Must:** Customer-only pages require authentication.
-   **ACC-04 --- Should:** Customer can update basic profile
    information.
-   **ACC-05 --- Must:** Use Django's built-in User model; no duplicate
    admin authentication table.
-   **ACC-06 --- Must:** Admin account uses `is_staff=True`.
-   **ACC-07 --- Must:** Admin module access is checked against assigned
    roles/permissions.
-   **ACC-08 --- Must:** Deactivate accounts with `is_active=False`; do
    not routinely hard-delete admin accounts.
-   **ACC-09 --- Must:** Guest checkout must not require registration.

### 4.2 Categories and SEO

-   **CAT-01 --- Must:** Authorized staff can create/view/update
    categories.
-   **CAT-02 --- Must:** Category has name, unique slug, description,
    active state and sort order.
-   **CAT-03 --- Must:** Category uses the abstract `HasSEO` model.
-   **CAT-04 --- Must:** Category supports soft delete, Trash, Restore
    and guarded Permanent Delete.
-   **CAT-05 --- Must:** Trashed/inactive categories do not appear in
    public navigation/filtering.
-   **CAT-06 --- Must:** Category with linked products cannot be
    permanently deleted until references are resolved.
-   **CAT-07 --- Must:** Soft-deleting a category does not
    cascade-delete its products.

### 4.3 Brands

-   **BRAND-01 --- Should:** Staff can manage brands.
-   **BRAND-02 --- Should:** Product may have an optional Brand.
-   **BRAND-03 --- Should:** Brand supports active/inactive state and
    recoverable deletion.
-   **BRAND-04 --- Must:** Brand cannot be permanently deleted while
    products reference it.

### 4.4 Products and `HasSEO`

-   **PROD-01 --- Must:** Staff can create/view/update products.
-   **PROD-02 --- Must:** Product has SKU, name, slug, category,
    optional brand, description, product type, pricing, shared stock,
    image and active state.
-   **PROD-03 --- Must:** Product supports `SIMPLE` and `OPTION_WISE`
    modes.
-   **PROD-04 --- Must:** Product uses abstract `HasSEO`.
-   **PROD-05 --- Must:** Public pages show only active/non-trashed
    products in active categories.
-   **PROD-06 --- Must:** Money uses DecimalField.
-   **PROD-07 --- Must:** Server validates price, options, product state
    and stock.
-   **PROD-08 --- Must:** Trashed/inactive products cannot be added to
    cart or checked out.
-   **PROD-09 --- Must:** Product supports soft delete, Trash, Restore
    and guarded Permanent Delete.
-   **PROD-10 --- Must:** Product referenced by historical Order Items
    cannot be permanently deleted if order history would be damaged.
-   **PROD-11 --- Must:** Order Items preserve product name, SKU, price
    and option snapshots.
-   **PROD-12 --- Should:** Product may include an optional downloadable
    datasheet/manual using Django `FileField`; product photos use
    `ImageField`.

`HasSEO` fields: `has_seo`, `meta_title`, `meta_description`,
`meta_keywords`, `canonical_url`, `og_title`, `og_description`,
`og_image`, `robots_index`, `robots_follow`. It is an abstract model and
creates no separate table.

### 4.5 Product Options and Option-wise Pricing

-   **OPT-01 --- Must:** Admin can manage global Color, Size, Weight and
    Piece Count option types.
-   **OPT-02 --- Must:** Option values have display label, unique code,
    sort order, active state and optional HEX swatch.
-   **OPT-03 --- Must:** Admin can assign multiple available values to a
    product's option groups.
-   **OPT-04 --- Must:** Product can enable/disable each option group
    and set required/optional status.
-   **OPT-05 --- Must:** Color, Size and Weight are optional on
    storefront.
-   **OPT-06 --- Must:** Piece Count is required for an option-wise
    product.
-   **OPT-07 --- Must:** Customer selects at most one value per
    displayed option group.
-   **OPT-08 --- Must:** Only Piece Count changes price in version 1.
-   **OPT-09 --- Must:** Color/Size/Weight do not create separate price
    rows or stock quantities in version 1.
-   **OPT-10 --- Must:** Admin sets a price and optional compare-at
    price for each Piece Count value assigned to a product.
-   **OPT-11 --- Must:** Unique product + Piece Count value price row.
-   **OPT-12 --- Must:** Server calculates price from
    ProductOptionPrice; never trust browser-submitted price.
-   **OPT-13 --- Must:** Product list/detail shows fixed price or
    option-wise starting price/range.
-   **OPT-14 --- Must:** Physical stock is shared at Product level.
-   **OPT-15 --- Must:** Cart/Order Items preserve selected options and
    price snapshots.
-   **OPT-16 --- Must:** Inactive/trashed option values cannot be newly
    selected.
-   **OPT-17 --- Must:** Option Type/Value cannot be permanently deleted
    while product configuration or price rows reference them.

  -----------------------------------------------------------------------
  Option            Example values    Storefront        Price effect v1
  ----------------- ----------------- ----------------- -----------------
  Color             Red, Black        Optional          No

  Size              M, L, XL          Optional          No

  Weight            5g, 10g           Optional          No

  Piece Count       1 Piece, 2        Required for      Yes
                    Pieces, 3 Pieces  option-wise       
                                      product           
  -----------------------------------------------------------------------

Admin may assign multiple values; customer chooses one value per option
group. This is option-wise pricing, not a separate SKU/stock row for
every combination.

### 4.6 Cart --- Guest and Registered

-   **CART-01 --- Must:** Registered customer can have a customer-owned
    cart.
-   **CART-02 --- Must:** Guest can have a session-owned cart.
-   **CART-03 --- Must:** Cart has exactly one owner: user XOR guest
    session key.
-   **CART-04 --- Must:** Cart Item stores product, quantity, selected
    options, configuration identity and price snapshot.
-   **CART-05 --- Must:** Different option configurations can be
    separate cart lines.
-   **CART-06 --- Must:** Identical product/option configurations are
    merged or quantity-updated.
-   **CART-07 --- Must:** Server calculates totals.
-   **CART-08 --- Must:** Checkout revalidates price, product state and
    shared stock.
-   **CART-09 --- Must:** Guest cart merges into customer cart after
    login.
-   **CART-10 --- Must:** Removing a cart item is a normal cart
    operation, not Trash.

### 4.7 Orders and Guest Checkout

-   **ORD-01 --- Must:** Guest and authenticated customers can both
    place orders.
-   **ORD-02 --- Must:** Order User FK is nullable.
-   **ORD-03 --- Must:** Order stores customer name, email, phone and
    shipping snapshots.
-   **ORD-04 --- Must:** Guest checkout requires no account creation.
-   **ORD-05 --- Must:** Guest order tracking requires order number plus
    email/phone verification or secure token.
-   **ORD-06 --- Must:** Registered customers can view only their own
    orders.
-   **ORD-07 --- Must:** Order and Order Items are created in a database
    transaction.
-   **ORD-08 --- Must:** Stock is rechecked and adjusted safely during
    checkout.
-   **ORD-09 --- Must:** Order Item stores product name, SKU, unit
    price, quantity, line total and option snapshots.
-   **ORD-10 --- Must:** Staff can update allowed order statuses with
    permission.
-   **ORD-11 --- Must:** Orders are retained and excluded from normal
    Trash/permanent delete.

### 4.8 Payments

-   **PAY-01 --- Must:** First version supports Cash on Delivery or
    mock/test payment.
-   **PAY-02 --- Must:** Store method, amount, status and optional
    transaction reference.
-   **PAY-03 --- Must:** Never store card number, CVV or sensitive card
    credentials.
-   **PAY-04 --- Must:** Retain payment records; exclude from normal
    Trash/permanent delete.
-   **PAY-05 --- Should:** Add a real gateway later using sandbox mode.

### 4.9 Reviews

-   **REV-01 --- Should:** Authenticated customer can submit
    rating/review.
-   **REV-02 --- Should:** Staff can moderate reviews.
-   **REV-03 --- Must:** Review supports soft delete, Trash, Restore and
    guarded Permanent Delete.
-   **REV-04 --- Must:** Trashed/inactive reviews are hidden publicly.

### 4.10 Site Settings

-   **SITE-01 --- Must:** Manage site name and tagline.
-   **SITE-02 --- Must:** Upload/change logo.
-   **SITE-03 --- Must:** Upload/change favicon/site icon.
-   **SITE-04 --- Must:** Manage contact email, phone and address.
-   **SITE-05 --- Must:** Manage footer about text, contact details and
    copyright.
-   **SITE-06 --- Must:** Manage dynamic footer sections and links,
    including sort order and active state.
-   **SITE-07 --- Must:** Shared frontend templates render current
    settings.
-   **SITE-08 --- Must:** Images live in media storage; DB stores file
    paths.

### 4.11 Admin Accounts, Roles and Permissions

-   **RBAC-01 --- Must:** Admin accounts use Django's built-in User
    model with `is_staff=True`.
-   **RBAC-02 --- Must:** Superuser status uses Django's `is_superuser`.
-   **RBAC-03 --- Must:** Authorized superusers/admin managers can
    create, view, update and deactivate admin accounts.
-   **RBAC-04 --- Must:** Integrate `django-role-permissions` (PyPI
    package name) and add `rolepermissions` to `INSTALLED_APPS`.
-   **RBAC-05 --- Must:** Define roles as `AbstractUserRole` classes in
    a project `roles.py` module, with explicit `available_permissions`.
-   **RBAC-06 --- Must:** Configure `ROLEPERMISSIONS_MODULE` to point to
    the project's roles module.
-   **RBAC-07 --- Must:** Use Django's built-in `auth_group` and
    `auth_permission` tables as the role/permission storage used by the
    package. Do not create duplicate custom
    AdminRole/AdminPermission/assignment tables.
-   **RBAC-08 --- Must:** The admin panel can list the predefined
    code-defined roles/permissions and assign/remove predefined roles
    to/from admin users.
-   **RBAC-09 --- Must:** Adding a new role or permission definition
    requires a code change in `roles.py` and running `sync_roles`;
    arbitrary new role classes are not created solely by a database
    form.
-   **RBAC-10 --- Must:** Use package helpers such as `has_permission()`
    and `has_role()` in server-side view/service checks.
-   **RBAC-11 --- Must:** `is_staff` gates access to Django Admin;
    superusers retain full access unless the package's superuser
    behavior is explicitly configured otherwise.
-   **RBAC-12 --- Must:** All sensitive actions still require explicit
    server-side authorization. Hiding menu items/buttons is not
    sufficient.
-   **RBAC-13 --- Must:** Admin accounts are deactivated rather than
    routinely hard-deleted, preserving audit history.

Example permission codenames include `product_view`, `product_create`,
`product_update`, `product_trash`, `product_restore`,
`product_force_delete`, `category_trash`, `audit_log_view`,
`site_settings_manage`, `tracking_settings_manage` and
`system_tools_manage`.

**Role lifecycle decision:** Since `django-role-permissions` defines
roles in Python code, role definitions are not part of the soft-delete
Trash workflow. Admin-role assignments can be revoked; code-defined
roles/permissions are changed through a reviewed code deployment and
`sync_roles`.

### 4.12 Audit Log

-   **AUD-01 --- Must:** Record actor, action, module, target model/ID
    and timestamp.
-   **AUD-02 --- Must:** Store before/after JSON for relevant updates
    where practical.
-   **AUD-03 --- Must:** Record Trash, Restore, Permanent Delete and
    bulk operations.
-   **AUD-04 --- Must:** Record admin account changes, role
    assignment/revocation changes and `sync_roles` executions.
    Code-defined role/permission changes are also tracked through
    Git/deployment history.
-   **AUD-05 --- Must:** Record site/tracking settings and System
    Command executions.
-   **AUD-06 --- Must:** Capture IP/user agent where available.
-   **AUD-07 --- Must:** Audit logs are append-only and not
    editable/deletable through normal admin UI.
-   **AUD-08 --- Must:** Redact passwords, tokens, card data and
    secrets.

### 4.13 Bulk Actions

-   **BULK-01 --- Must:** Admin lists support multi-select.
-   **BULK-02 --- Must:** Bulk Move to Trash for eligible models.
-   **BULK-03 --- Must:** Bulk Restore from Trash.
-   **BULK-04 --- Must:** Bulk Permanent Delete is superuser-only and
    requires confirmation.
-   **BULK-05 --- Must:** Bulk activate/deactivate or safe status
    updates where applicable.
-   **BULK-06 --- Must:** Validate each selected record's permissions
    and relationships.
-   **BULK-07 --- Must:** Show requested/success/skipped/failed counts.
-   **BULK-08 --- Must:** Store a batch summary and per-object audit
    entries.
-   **BULK-09 --- Must:** One failed item must not silently corrupt
    other records.

### 4.14 System Commands for cPanel

-   **CMD-01 --- Must:** Provide System Commands page for cPanel where
    terminal access is unavailable.
-   **CMD-02 --- Must:** Execute only predefined Django management
    commands via `django.core.management.call_command`.
-   **CMD-03 --- Must:** No arbitrary shell command, Python expression
    or raw SQL input.
-   **CMD-04 --- Must:** Require superuser or `system_tools_manage`.
-   **CMD-05 --- Must:** Use POST, CSRF and explicit confirmation for
    state-changing commands.
-   **CMD-06 --- Must:** Log actor, command, environment, status,
    timestamps and sanitized output.
-   **CMD-07 --- Must:** Production allowlist may include `check`,
    `showmigrations`, `migrate`, `collectstatic`, `clearsessions` and
    `sync_roles`.
-   **CMD-08 --- Must:** Production `migrate` requires superuser,
    confirmation and backup warning.
-   **CMD-09 --- Must:** Destructive DB commands such as `flush`/reset
    are disabled in production.
-   **CMD-10 --- Must:** Run `makemigrations` locally and deploy
    migration files with code.
-   **CMD-11 --- Must:** Apply execution time and output-size limits.

### 4.15 Meta Pixel and CAPI

-   **TRACK-01 --- Must:** Admin can enable/disable Pixel and configure
    Pixel ID.
-   **TRACK-02 --- Must:** Pixel script loads from shared templates when
    enabled and consent allows.
-   **TRACK-03 --- Must:** Support PageView, ViewContent, AddToCart,
    InitiateCheckout and Purchase.
-   **TRACK-04 --- Must:** CAPI sends server-side events for supported
    actions.
-   **TRACK-05 --- Must:** Browser/server copies share `event_id` for
    deduplication.
-   **TRACK-06 --- Must:** CAPI token is stored in server
    environment/secret storage, never frontend code or ordinary DB
    settings.
-   **TRACK-07 --- Must:** Store delivery status, attempts and sanitized
    response details.
-   **TRACK-08 --- Must:** Do not log access tokens, passwords, card
    data or unnecessary raw personal data.
-   **TRACK-09 --- Must:** Hash permitted identifiers as required and
    respect consent/privacy.
-   **TRACK-10 --- Should:** Support Meta Test Event Code in test
    configuration.

------------------------------------------------------------------------

## 5. Soft Delete, Trash, Restore and Permanent Delete

### 5.1 Shared model

Use abstract `SoftDeleteModel` in `core`: - `is_deleted` Boolean,
default False - `deleted_at` nullable DateTime - `deleted_by` nullable
FK to User, `SET_NULL`

It creates no separate table.

### 5.2 Eligible models

Mandatory: Category and Product.

Also eligible: Brand, OptionType, OptionValue and Review. Role
definitions and permission codenames are code-managed by
django-role-permissions and Django Groups/Permissions; they are not
custom soft-deletable records.

### 5.3 Protected records

-   Admin accounts: deactivate using `is_active=False`.
-   Orders and Payments: retain; use status changes.
-   Audit Logs and System Command Run records: append-only/retained.
-   Cart Items: remove normally.

### 5.4 Move to Trash

Set `is_deleted=True`, `deleted_at=now`, `deleted_by=actor`; do not
physically delete. Hide from public pages and normal active lists. Write
an audit entry.

### 5.5 Trash and Restore

Trash filters by model/module and shows record label, deletion time and
actor. Restore clears all soft-delete fields and validates unique
slug/code and relationship constraints. If restore conflicts, leave the
record in Trash and show a clear error.

### 5.6 Permanent Delete

-   Superuser only.
-   Available only from Trash.
-   Separate confirmation page/message.
-   Validate foreign-key relationships before deletion.
-   Block Category deletion while Products reference it.
-   Block Product deletion while Order Items reference it.
-   Role definitions are code-managed; do not expose role/permission
    definitions as Trash records. Revoke role assignments through
    authorized admin actions, and update role definitions through code
    deployment plus `sync_roles`.
-   Block Option Type/Value deletion while product groups/prices
    reference them.
-   Preserve Orders, Payments, Audit Logs and System Command history.

### 5.7 Bulk operations

Validate each selected row, report partial failures, record per-object
audit entries and a batch summary. Backend authorization is mandatory;
hiding a UI button is not security.

------------------------------------------------------------------------

## 6. Business and Data Integrity Rules

1.  Use DecimalField for all money.
2.  Option-wise price comes from Product + selected Piece Count value.
3.  Color/Size/Weight do not affect price in version 1.
4.  Stock is shared at Product level.
5.  Cart line identity includes the selected option configuration.
6.  Order Items preserve product, SKU, price and option snapshots.
7.  Guest Order has nullable User FK and mandatory checkout
    contact/shipping snapshots.
8.  Use transactions for checkout and stock updates.
9.  Use protective FKs for historical order/payment records.
10. Category soft delete does not cascade-delete Product.
11. Public querysets exclude inactive/trashed records.

## 7. Non-Functional Requirements

-   Keep `.env` out of Git.
-   Use Django password hashing and CSRF protection.
-   Enforce roles/permissions server-side.
-   Validate user input, stock and price on server.
-   Keep Audit Logs append-only.
-   Never expose CAPI token or card data.
-   Use HTTPS and `DEBUG=False` in production.
-   Do not rely on cPanel shell access; use the restricted command
    runner.
-   Test permissions, guest checkout, price integrity, soft delete,
    restore, permanent delete, bulk actions and tracking deduplication.

## 8. Acceptance Criteria

### Product and options

-   [ ] Category and Product have HasSEO fields.
-   [ ] Category and Product support soft delete.
-   [ ] Simple and option-wise products work.
-   [ ] Color/Size/Weight are optional.
-   [ ] Piece Count is required for option-wise products.
-   [ ] Only Piece Count changes price in version 1.
-   [ ] Stock is shared at Product level.
-   [ ] Cart/order preserves option and price snapshots.

### Checkout

-   [ ] Guest can buy without account.
-   [ ] Registered customer can buy and view own order history.
-   [ ] Guest order tracking requires verification.
-   [ ] Guest cart merges after login.
-   [ ] Checkout revalidates price and stock.

### Admin

-   [ ] Admin accounts, roles and permissions work.
-   [ ] Server-side permission checks protect all actions.
-   [ ] Audit Log records important changes.
-   [ ] Bulk Trash/Restore works.
-   [ ] Bulk Permanent Delete is superuser-only and confirmed.
-   [ ] FK safeguards protect order/payment history.

### Site, tracking and deployment

-   [ ] Logo, favicon, contact and footer are editable.
-   [ ] Meta Pixel browser events work when enabled/consented.
-   [ ] CAPI server events work and deduplicate by event_id.
-   [ ] CAPI token is never exposed in frontend/database output.
-   [ ] System Commands runs only approved commands.
-   [ ] Production destructive commands are blocked.
-   [ ] Command runs are audited.

### Technical

-   [ ] MySQL migrations pass.
-   [ ] `.env` is not committed.
-   [ ] Tests cover critical flows and permissions.
-   [ ] Production uses secure settings.

## 9. Development Plan

1.  Foundation and core abstract models.
2.  Categories, Brand, Product and SEO.
3.  Option types/values, product option groups and Piece Count prices.
4.  Accounts, guest cart and customer cart.
5.  Cart option snapshots, server-side pricing and stock checks.
6.  Guest/registered checkout, orders, stock movement and payments.
7.  Reviews.
8.  Admin accounts, roles, permissions, audit and bulk actions.
9.  Trash/Restore/Permanent Delete safeguards.
10. Site Settings and footer.
11. Meta Pixel and CAPI.
12. System Commands and cPanel deployment.
13. Testing and security review.

## 10. Out of Scope for Version 1

-   Separate stock per option combination.
-   Price changes for Color, Size or Weight.
-   SKU per possible option combination.
-   Live card processing or storing card credentials.
-   Multi-vendor marketplace and complex warehouse integrations.
-   Arbitrary browser-based shell access.
-   Permanent deletion of orders, payments, audit logs or command
    history.
-   Advanced analytics beyond the initial Meta event set.

------------------------------------------------------------------------

## 11. Starter Project Configuration Note

The supplied starter `manage.py` references `demoApp.settings`. The
target architecture uses `config` as the Django project package. During
implementation, keep `manage.py`, ASGI, WSGI, `ROOT_URLCONF` and the
actual project package name aligned. If retaining `demoApp`, keep that
package name consistently; if switching to `config`, update all related
project references together.

The cPanel System Commands feature is separate from `manage.py`: it must
call only predefined Django management commands through
`django.core.management.call_command`, never arbitrary shell input.

------------------------------------------------------------------------

## 12. Required Package Integration

### 12.1 `django-role-permissions`

-   PyPI install name: `django-role-permissions`.
-   Django app label: `rolepermissions`.
-   Role classes are defined in `roles.py` using `AbstractUserRole`.
-   `available_permissions` defines the permission codenames and
    defaults for each role.
-   Set `ROLEPERMISSIONS_MODULE` to the module path, for example
    `config.roles` if the project package is `config`.
-   Use `assign_role`, `remove_role`, `has_role` and `has_permission`
    for assignment and authorization.
-   Use `sync_roles` to synchronize role definitions to Django's
    Groups/Permissions.
-   This is code-defined RBAC. The custom admin UI may manage
    assignments and display definitions, but it must not imply that
    arbitrary role classes can be created dynamically from a database
    form.

### 12.2 `django-jazzmin`

-   PyPI install name: `django-jazzmin`.
-   Django app label: `jazzmin`.
-   Add `jazzmin` before `django.contrib.admin` in `INSTALLED_APPS`.
-   Configure the admin title, logo, icons, menu and UI through Jazzmin
    settings.
-   Jazzmin themes Django's built-in Admin; custom dashboard views need
    their own Bootstrap 5 templates and authorization.

### 12.3 Django FileField / ImageField

-   `FileField` and `ImageField` are built into Django; they are not
    separate pip packages.
-   Use `ImageField` for product/brand/site/SEO images and `FileField`
    for generic documents such as a product datasheet PDF.
-   Configure `MEDIA_ROOT` and `MEDIA_URL`.
-   Install Pillow for image uploads.
-   Validate upload size, extension and actual file content on the
    server.
-   Store only the file path in MySQL; the file bytes live in the
    configured storage backend.
-   Ensure cPanel media directories are writable and included in
    backups.

### 12.4 Compatibility Verification Gate

The current target is Django 6.1.3. At the time this document was
updated: - `django-role-permissions` latest published version found was
3.2.0 (June 2023); recent maintenance activity is low/dormant. -
`django-jazzmin` latest published version found was 3.0.5 (June 2026);
its PyPI classifiers list Django through 6.0, not 6.1.

Therefore, package installation success alone is not proof of runtime
compatibility. Before implementation proceeds, run `manage.py check`,
verify Jazzmin admin rendering, verify `sync_roles`, test role
assignment and permission decorators/checkers, and test media uploads
under the exact Django version. Do not upgrade/downgrade Django without
a deliberate compatibility decision.

### 4.16 Django Admin UI Theme --- Jazzmin

-   **JAZZ-01 --- Must:** Use `django-jazzmin` to theme Django's
    built-in Admin.
-   **JAZZ-02 --- Must:** Add `jazzmin` before `django.contrib.admin` in
    `INSTALLED_APPS`.
-   **JAZZ-03 --- Should:** Configure site title, logo, favicon, menu
    labels, icons and UI tweaks through Jazzmin settings.
-   **JAZZ-04 --- Must:** Do not assume Jazzmin automatically styles
    custom `dashboard` app views; custom dashboard pages must use their
    own Bootstrap 5 templates and server-side permission checks.
-   **JAZZ-05 --- Must:** Verify Jazzmin static assets with
    `collectstatic` and test the admin UI under the selected Django
    version.

## 13. Official Package and Framework References

-   Django FileField:
    https://docs.djangoproject.com/en/6.1/ref/models/fields/#filefield
-   Django file uploads:
    https://docs.djangoproject.com/en/6.1/topics/files/
-   django-role-permissions:
    https://django-role-permissions.readthedocs.io/en/stable/
-   django-role-permissions PyPI:
    https://pypi.org/project/django-role-permissions/
-   Jazzmin installation:
    https://django-jazzmin.readthedocs.io/installation/
-   Jazzmin PyPI: https://pypi.org/project/django-jazzmin/
