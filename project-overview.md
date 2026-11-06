# Ecommerce Practice Project --- Overview

**Document version:** 2.1\
**Project:** Ecommerce\
**Type:** Small modular e-commerce application\
**Stack:** Python 3.12, Django 6.1.3, Django ORM, MySQL 8.4,
`mysqlclient`, `django-role-permissions`, `django-jazzmin`, Django
`FileField`/`ImageField`, Pillow, Django Templates, HTML, CSS, Bootstrap
and JavaScript.

## 1. Purpose and Goals

Build a small but realistic e-commerce application for practising
Django, MySQL, authentication, CRUD, relationships, pricing, order
processing, admin security and deployment.

The project must: - Provide categories, brands, products, product
options and SEO. - Support simple and option-wise products. - Allow both
guest and registered customers to purchase. - Provide cart, checkout,
order and payment workflows. - Provide Category/Product soft delete with
Trash, Restore and Permanent Delete. - Provide admin accounts, roles,
permissions, audit logs and bulk actions. - Manage site logo,
favicon/site icon, contact details and footer information. - Support
Meta Pixel browser tracking and Meta Conversions API (CAPI). - Provide a
secure System Command Runner for cPanel deployments without terminal
access.

Develop and test one app/feature group at a time.

## 2. Technology and Supporting Packages

### Core stack

-   Python 3.12
-   Django 6.1.3 (current project target; keep the exact tested version
    in `requirements.txt`)
-   MySQL 8.4 with `mysqlclient`
-   Django Templates, HTML, CSS, Bootstrap and JavaScript
-   `python-dotenv` or hosting environment variables
-   Git; `.env` must never be committed

### Required Django packages

  --------------------------------------------------------------------------
  Package / feature           Purpose           Installation / import
  --------------------------- ----------------- ----------------------------
  `django-role-permissions`   Role-based        PyPI:
                              authorization     `django-role-permissions`;
                              using Django      app: `rolepermissions`
                              Groups and        
                              Permissions       

  `django-jazzmin`            Theme for         PyPI: `django-jazzmin`; app:
                              Django's built-in `jazzmin`
                              Admin UI          

  Django `FileField`          Generic file      Built into Django; no
                              uploads such as   separate package
                              product           
                              datasheets/PDFs   

  Django `ImageField`         Product images,   Built into Django; install
                              brand logos, site Pillow
                              logo, favicon and 
                              SEO images        
  --------------------------------------------------------------------------

Additional packages: - `Pillow` for image validation and `ImageField`. -
`requests` or an equivalent maintained HTTP client for Meta CAPI.

### Candidate package versions and compatibility gate

-   `django-role-permissions==3.2.0` is the latest published release
    found for this review, but its last release was in June 2023 and
    package activity is dormant. Its compatibility with Django 6.1.3
    must be tested before relying on it in production.
-   `django-jazzmin==3.0.5` is the latest release found for this review.
    Its published Django classifiers list support through Django 6.0,
    not 6.1; Django 6.1.3 compatibility is therefore not officially
    declared in the package metadata.
-   Do not silently downgrade Django or assume compatibility. First
    install these candidate versions in the development virtual
    environment, then run Django checks, admin smoke tests, role
    assignment tests and file-upload tests. If a package fails, decide
    whether to use a compatible Django release or replace that
    integration before building dependent features.

Candidate install command:

``` powershell
python -m pip install "django-role-permissions==3.2.0" "django-jazzmin==3.0.5" Pillow
```

`FileField` and `ImageField` are Django model fields, not third-party
packages. Uploaded file bytes are stored through Django's configured
storage; MySQL stores the file path/name, not the file contents.

Keep all tested exact dependency versions in `requirements.txt`.

## 3. Target Project Structure

``` text
Ecommerce/
├── .venv/
├── config/                 # Settings, root URLs, ASGI and WSGI
├── core/                   # Abstract models, managers and shared utilities
├── accounts/               # Customer authentication and profiles
├── categories/             # Categories and category SEO
├── products/               # Products, brands, options, pricing and stock
├── cart/                   # Guest and registered-user carts
├── orders/                 # Checkout, orders and order items
├── payments/               # Payment methods and payment status
├── reviews/                # Product reviews and moderation
├── dashboard/              # Admins, RBAC, audit, bulk actions, commands
├── site_settings/          # Logo, favicon, contact and footer settings
├── tracking/               # Meta Pixel, CAPI and event logs
├── templates/
├── static/
├── media/
├── .env
├── .gitignore
├── requirements.txt
├── manage.py
├── project-overview.md
├── Ecommerce_PRD.md
├── ERD.md
└── database-schema.md
```

## 4. Django App Responsibilities

  ---------------------------------------------------------------------
  App                                Responsibility
  ---------------------------------- ----------------------------------
  `config`                           Django settings, root URL routing,
                                     ASGI and WSGI

  `core`                             Abstract `SoftDeleteModel`,
                                     abstract `HasSEO`, managers and
                                     helpers

  `accounts`                         Registration, login, logout,
                                     customer profile and account state

  `categories`                       Category CRUD, visibility and SEO

  `products`                         Product, Brand, option
                                     types/values, option groups,
                                     option-wise pricing and stock

  `cart`                             Guest/session carts, customer
                                     carts, cart items and selected
                                     options

  `orders`                           Guest/registered checkout, orders,
                                     order items and tracking

  `payments`                         COD/mock payment and payment
                                     status

  `reviews`                          Customer reviews and moderation

  `dashboard`                        Admin accounts, custom
                                     roles/permissions, audit logs,
                                     bulk actions and System Commands

  `site_settings`                    Site name, logo, favicon, contact
                                     details and footer

  `tracking`                         Meta Pixel, CAPI, event
                                     deduplication and event logs
  ---------------------------------------------------------------------

Do not create additional apps for every small feature. Keep the
responsibilities above unless implementation shows a clear need to
change them.

## 5. Users and Purchase Access

### Visitor / Guest Buyer

-   Browse active categories and products.
-   View product details and available options.
-   Use a session-based cart.
-   Complete checkout without creating an account.
-   Track an order using its order reference plus email/phone
    verification or a secure guest token.

### Registered Customer

-   Register, log in and log out.
-   Use a customer-owned cart and place orders.
-   View only their own order history.
-   Submit reviews where enabled.
-   Merge eligible guest-cart items into their customer cart after
    login.

### Staff / Admin / Superuser

-   Admin accounts use Django's built-in User model with
    `is_staff=True`.
-   Custom roles and permissions control access to admin
    modules/actions.
-   Superusers have full access and may permanently delete eligible
    trashed records after confirmation.
-   Admin accounts are deactivated rather than routinely hard-deleted.

## 6. Product Options and Option-wise Pricing

Products support two modes:

1.  **Simple product:** Uses its normal `base_price`.
2.  **Option-wise product:** Uses a price row for each available Piece
    Count value.

  -----------------------------------------------------------------------
  Option                  Storefront selection    Changes price in
                                                  version 1?
  ----------------------- ----------------------- -----------------------
  Color                   Optional; select one    No
                          value or skip           

  Size                    Optional; select one    No
                          value or skip           

  Weight                  Optional; select one    No
                          value or skip           

  Piece Count             Required for            Yes
                          option-wise products;   
                          select one value        
  -----------------------------------------------------------------------

Example values: - Color: Red, Black - Size: M, L, XL - Weight: 5g, 10g -
Piece Count: 1 Piece, 2 Pieces, 3 Pieces

Admin assigns available values to each product option group. Customers
choose at most one value from each displayed group. In version 1, only
Piece Count changes the price; Color, Size and Weight are descriptive
selections.

**Stock is shared at Product level.** Do not create separate stock
quantities or a separate SKU for every possible option combination in
version 1. Cart and Order Items preserve the selected options and price
snapshots.

## 7. SEO --- `HasSEO`

Use a reusable Django abstract model named `HasSEO` for Category and
Product. It provides:

-   `has_seo`
-   `meta_title`
-   `meta_description`
-   `meta_keywords`
-   `canonical_url`
-   `og_title`
-   `og_description`
-   `og_image`
-   `robots_index`
-   `robots_follow`

`HasSEO` is an abstract model/mixin, not a separate database table. When
custom SEO is disabled, the frontend can use site-level defaults.

## 8. Soft Delete and Trash

Use a reusable abstract `SoftDeleteModel` with: - `is_deleted` -
`deleted_at` - `deleted_by`

Category and Product soft delete is mandatory. Also support recoverable
deletion for eligible Brand, OptionType, OptionValue and Review records.
Role definitions and permissions are code-managed through
django-role-permissions and Django Groups/Permissions, not custom
soft-deletable tables.

``` text
Active → Move to Trash → Trashed
                         ├── Restore → Active
                         └── Superuser confirmation → Permanent Delete
```

-   Normal lists/public pages exclude trashed records.
-   Trash explicitly lists trashed records.
-   Restore clears soft-delete fields.
-   Permanent Delete is superuser-only, from Trash, after confirmation.
-   Bulk Trash, Bulk Restore and Bulk Permanent Delete are available for
    eligible records.
-   Orders, Payments, Audit Logs and System Command history are
    retained.
-   Admin accounts are deactivated, not deleted.
-   Foreign-key protections preserve order/payment/audit history.

## 9. Admin Panel

The `dashboard` app provides:

### Admin accounts

-   Create, view, update and deactivate admin accounts.
-   Use Django User with `is_staff`; do not duplicate authentication
    tables.

### Roles and permissions

-   Use `django-role-permissions` as the role/permission checking layer.
-   Define role classes and their `available_permissions` in a project
    `roles.py` module.
-   Configure `ROLEPERMISSIONS_MODULE` to point to that module.
-   The package uses Django's built-in `Group` and `Permission` records;
    do not create duplicate `AdminRole`, `AdminPermission`,
    `AdminUserRole` or `AdminRolePermission` tables.
-   The admin panel can list the predefined roles/permissions and
    assign/remove predefined roles for admin users.
-   New role definitions or new permission codenames require a code
    change in `roles.py` followed by the package's `sync_roles`
    management command.
-   Enforce `has_permission()` / `has_role()` checks server-side on
    every protected dashboard view and action.
-   Django `is_staff` gates admin-site access; `is_superuser` is the
    emergency/full-access account.
-   Jazzmin themes Django's built-in Admin. Custom dashboard views must
    use their own Bootstrap 5 templates and permission checks; Jazzmin
    does not automatically theme arbitrary custom pages.

### Audit Log

Record actor, action, module, target object, timestamp, before/after
data where appropriate, IP and user agent. Log create/update, Trash,
Restore, Permanent Delete, role assignment/revocation changes, admin
changes, bulk actions, settings/tracking changes and System Command
executions.

Audit Logs are append-only in the application. Never log passwords, CAPI
tokens or payment-card data.

### Bulk Actions

Support multi-select operations: - Move to Trash - Restore - Permanently
Delete (superuser only, confirmation required) - Activate/Deactivate or
other safe status changes

Show requested, successful, skipped and failed counts. Record per-object
audit events and a batch summary.

## 10. Site Settings

The `site_settings` app manages a singleton-style `SiteSettings`
record: - Site name and tagline - Header logo - Favicon/site icon -
Contact email, phone and address - Footer about text, contact details
and copyright text - Social links - Dynamic footer sections and links -
Default SEO title, description and Open Graph image

Use `FooterSection` and `FooterLink` for editable footer columns/links.
Store uploaded files in media storage and only file paths in MySQL.

## 11. Meta Pixel and Conversions API

The `tracking` app supports: - Configurable Pixel ID and enable/disable
setting. - Browser Pixel script in shared frontend templates. - Events:
PageView, ViewContent, AddToCart, InitiateCheckout and Purchase. -
Server-side CAPI events for supported actions. - Same `event_id` for
browser and server copies to enable deduplication. - CAPI access token
stored only in server environment variables/secure secret storage. -
Event delivery logs with sanitized response summaries. -
Normalized/hashed permitted customer identifiers where required. - No
passwords, card numbers, CVV or unnecessary sensitive personal data. -
Consent/privacy controls.

## 12. cPanel System Command Runner

The `dashboard` app provides a System Commands page for cPanel
environments without terminal access.

-   Execute only predefined, allowlisted Django commands using
    `django.core.management.call_command`.
-   Never accept arbitrary shell commands, Python expressions or raw
    SQL.
-   Suggested production allowlist: `check`, `showmigrations`,
    `migrate`, `collectstatic`, `clearsessions`.
-   Production `migrate` requires superuser, explicit confirmation and
    backup warning.
-   Destructive DB commands such as `flush`/reset are disabled in
    production.
-   Run `makemigrations` locally and deploy migration files with the
    code.
-   Use POST, CSRF protection, permission checks, time/output limits and
    audit logging.
-   Store actor, command code, environment, status, timestamps and
    sanitized output.

## 13. Main Customer Workflow

1.  Visitor browses active products/categories.
2.  Visitor opens a product.
3.  For option-wise products, visitor selects Piece Count and optionally
    Color, Size and Weight.
4.  Server calculates the price from the selected Piece Count.
5.  Product is added to a guest or registered cart.
6.  Customer checks out as guest or authenticated user.
7.  Server revalidates product status, price and shared stock.
8.  Order and Order Items are created in a database transaction with
    option/price snapshots.
9.  Payment status is recorded using COD or a mock/test flow.
10. Customer views their order, or a guest tracks it using verified
    details.
11. Pixel and CAPI events are sent according to settings and consent.

## 14. Development Phases

1.  Foundation, MySQL and shared `core` models.
2.  Categories, Brand, Product, SEO and soft delete.
3.  Option types/values, product option groups and Piece Count pricing.
4.  Accounts, guest cart and customer cart.
5.  Cart option snapshots, price calculation and stock validation.
6.  Guest/registered checkout, orders, stock movement and payments.
7.  Reviews.
8.  Admin accounts, roles, permissions, audit log, Trash and bulk
    actions.
9.  Site Settings and footer.
10. Meta Pixel and CAPI.
11. System Commands and cPanel deployment.
12. Testing and security cleanup.

## 15. Definition of Done --- First Practice Release

-   Guest and registered customers can both place orders.
-   Option-wise products support optional Color/Size/Weight and required
    Piece Count.
-   Piece Count determines price; stock is shared at product level.
-   Category and Product support Trash, Restore and guarded Permanent
    Delete.
-   Admin roles, permissions, audit logs and bulk actions work with
    server-side authorization.
-   Site logo, favicon and footer are editable.
-   Meta Pixel and CAPI events are configured and deduplicated.
-   System Commands runs only approved Django commands in cPanel.
-   MySQL migrations, permission tests and data-integrity tests pass.

## 16. Current Starter Workspace Alignment

The supplied starter `manage.py` currently sets `DJANGO_SETTINGS_MODULE`
to `demoApp.settings`, while the target structure in this documentation
uses the project package name `config`.

Before creating the final Ecommerce project, choose one consistent
project package:

-   Keep `demoApp` and keep `DJANGO_SETTINGS_MODULE='demoApp.settings'`;
    or
-   Use `config` and update `manage.py`, `config/asgi.py`,
    `config/wsgi.py`, `ROOT_URLCONF` and related references together.

Do not change only `manage.py` while leaving the other project
references unchanged. The uploaded `manage.py` is the standard Django
command entry point; the cPanel System Command Runner is a separate
admin feature that uses Django's allowlisted `call_command` API.

## 17. Package Integration and File Upload Rules

### `django-role-permissions`

-   Install the PyPI package `django-role-permissions`; add
    `rolepermissions` to `INSTALLED_APPS`.
-   Define roles in `config/roles.py` if the Django project package is
    named `config`. If the current project package remains `demoApp`,
    use `demoApp.roles` instead.
-   Set `ROLEPERMISSIONS_MODULE` to the matching Python module path.
-   Use `AbstractUserRole`, `available_permissions`, `assign_role`,
    `remove_role`, `has_role` and `has_permission` as appropriate.
-   Use the package's `sync_roles` command to synchronize code-defined
    roles/permissions to Django Groups/Permissions.
-   This package's roles are code-defined. Do not promise fully dynamic
    creation of arbitrary role definitions from the database admin UI.
-   The package is an authorization helper, not a replacement for
    server-side checks, audit logging or data-integrity rules.

### `django-jazzmin`

-   Install `django-jazzmin` and put `'jazzmin'` before
    `'django.contrib.admin'` in `INSTALLED_APPS`.
-   Configure branding, logo, site title, icons, side menu and top menu
    through `JAZZMIN_SETTINGS` / `JAZZMIN_UI_TWEAKS`.
-   Use Jazzmin for Django's built-in Admin interface.
-   Custom `dashboard` app pages are ordinary Django views/templates;
    style them with Bootstrap 5 and apply the same permissions
    explicitly.
-   Verify the installed Jazzmin release against the selected Django
    version before production deployment.

### Django `FileField` / `ImageField`

-   Use `ImageField` for product images, brand logos, site logo, favicon
    and Open Graph images.
-   Use `FileField` for optional product documents/datasheets or other
    generic files.
-   Configure `MEDIA_ROOT` and `MEDIA_URL`; ensure the cPanel web
    application user can write to the media directory.
-   Store uploads under controlled `upload_to` paths, validate
    extension/content type and file size, and generate safe filenames.
-   Database rows store file paths; file bytes are stored by Django's
    storage backend.
-   Add Pillow for `ImageField`.
-   Back up media files separately from the MySQL database. Do not place
    secrets or private documents in public media paths.

### Official references

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
