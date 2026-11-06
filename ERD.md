# Entity Relationship Diagram (ERD)

## Ecommerce Practice Project

**Document version:** 2.1\
**Database:** MySQL 8.4\
**Backend:** Django ORM

------------------------------------------------------------------------

## 1. Purpose and Design Notes

This is the logical ERD for the planned Ecommerce application. It
follows the updated Project Overview and PRD and the supplied
product/admin reference screenshots. It is a design blueprint, not a
database export.

Key decisions: - Django's built-in User model is the identity table for
customers and admins. - Guest carts and guest orders are supported
without a User FK. - Category and Product use `SoftDeleteModel` and
`HasSEO`. - Option-wise pricing is stored per Piece Count value. Color,
Size and Weight are optional and do not change price in version 1. -
Stock is shared at Product level. - Admin roles and permission codes use
custom RBAC tables. - Trash is a filtered view of soft-deleted rows, not
a separate Trash table. - Orders, Payments, Audit Logs and System
Command history are retained.

## 2. Main ERD --- Mermaid

``` mermaid
erDiagram
    AUTH_USER {
        bigint id PK
        string username UK
        string email
        string password
        boolean is_active
        boolean is_staff
        boolean is_superuser
    }

    ADMIN_PROFILE {
        bigint id PK
        bigint user_id FK_UK
        string phone
        string designation
        string avatar
    }

    AUTH_GROUP {
        bigint id PK
        string name UK
    }

    CONTENT_TYPE {
        bigint id PK
        string app_label
        string model
    }

    AUTH_PERMISSION {
        bigint id PK
        bigint content_type_id FK
        string codename
        string name
    }

    AUTH_USER_GROUPS {
        bigint id PK
        bigint user_id FK
        bigint group_id FK
    }

    AUTH_GROUP_PERMISSIONS {
        bigint id PK
        bigint group_id FK
        bigint permission_id FK
    }

    CATEGORY {
        bigint id PK
        string name
        string slug UK
        boolean is_active
        boolean is_deleted
        boolean has_seo
        string meta_title
        string meta_description
        datetime deleted_at
        bigint deleted_by_id FK
    }

    BRAND {
        bigint id PK
        string name
        string slug UK
        boolean is_active
        boolean is_deleted
        datetime deleted_at
        bigint deleted_by_id FK
    }

    PRODUCT {
        bigint id PK
        bigint category_id FK
        bigint brand_id FK
        string sku UK
        string name
        string slug UK
        string product_type
        decimal base_price
        integer stock_quantity
        string image_path
        string document_path
        boolean is_active
        boolean is_deleted
        boolean has_seo
        string meta_title
        string meta_description
        datetime deleted_at
        bigint deleted_by_id FK
    }

    OPTION_TYPE {
        bigint id PK
        string name
        string code UK
        boolean affects_price
        boolean is_required_by_default
        boolean is_active
        boolean is_deleted
    }

    OPTION_VALUE {
        bigint id PK
        bigint option_type_id FK
        string display_label
        string unique_code
        string swatch_hex
        integer sort_order
        boolean is_active
        boolean is_deleted
    }

    PRODUCT_OPTION_GROUP {
        bigint id PK
        bigint product_id FK
        bigint option_type_id FK
        boolean is_required
        integer sort_order
    }

    PRODUCT_OPTION_VALUE {
        bigint id PK
        bigint product_option_group_id FK
        bigint option_value_id FK
        integer sort_order
    }

    PRODUCT_OPTION_PRICE {
        bigint id PK
        bigint product_id FK
        bigint piece_count_value_id FK
        decimal price
        decimal compare_at_price
        boolean is_active
    }

    CART {
        bigint id PK
        bigint user_id FK
        string session_key UK
        datetime expires_at
        datetime updated_at
    }

    CART_ITEM {
        bigint id PK
        bigint cart_id FK
        bigint product_id FK
        integer quantity
        string configuration_hash
        decimal unit_price_snapshot
    }

    CART_ITEM_OPTION {
        bigint id PK
        bigint cart_item_id FK
        bigint option_type_id FK
        bigint option_value_id FK
    }

    CUSTOMER_ORDER {
        bigint id PK
        bigint user_id FK
        string order_number UK
        string customer_name
        string customer_email
        string customer_phone
        decimal total_amount
        string status
        string guest_tracking_token_hash
        datetime created_at
    }

    ORDER_ITEM {
        bigint id PK
        bigint order_id FK
        bigint product_id FK
        string product_name_snapshot
        string sku_snapshot
        decimal unit_price_snapshot
        integer quantity
        decimal line_total
    }

    ORDER_ITEM_OPTION {
        bigint id PK
        bigint order_item_id FK
        string option_type_name_snapshot
        string option_value_label_snapshot
        string option_value_code_snapshot
    }

    PAYMENT {
        bigint id PK
        bigint order_id FK_UK
        string payment_method
        decimal amount
        string transaction_reference
        string status
    }

    REVIEW {
        bigint id PK
        bigint user_id FK
        bigint product_id FK
        integer rating
        text comment
        boolean is_deleted
        datetime deleted_at
        bigint deleted_by_id FK
    }

    STOCK_MOVEMENT {
        bigint id PK
        bigint product_id FK
        bigint order_id FK
        bigint performed_by_id FK
        string movement_type
        integer quantity_delta
        integer stock_before
        integer stock_after
        datetime created_at
    }

    SITE_SETTINGS {
        bigint id PK
        string site_name
        string logo_path
        string favicon_path
        text footer_about
        string footer_email
        string footer_phone
        string footer_copyright
        bigint updated_by_id FK
    }

    FOOTER_SECTION {
        bigint id PK
        string title
        integer sort_order
        boolean is_active
    }

    FOOTER_LINK {
        bigint id PK
        bigint section_id FK
        string label
        string url
        integer sort_order
        boolean is_active
    }

    TRACKING_SETTINGS {
        bigint id PK
        string meta_pixel_id
        boolean pixel_enabled
        boolean capi_enabled
        boolean track_page_view
        boolean track_view_content
        boolean track_add_to_cart
        boolean track_checkout
        boolean track_purchase
        bigint updated_by_id FK
    }

    META_EVENT_LOG {
        bigint id PK
        string event_id UK
        string event_name
        bigint order_id FK
        string delivery_status
        integer attempts
        integer http_status
        datetime sent_at
    }

    AUDIT_LOG {
        bigint id PK
        bigint actor_id FK
        string action
        string module
        string target_model
        string target_object_id
        json before_data
        json after_data
        string ip_address
        datetime created_at
    }

    BULK_ACTION_BATCH {
        bigint id PK
        bigint initiated_by_id FK
        string model_label
        string action
        integer requested_count
        integer success_count
        integer failed_count
        json result_summary
        datetime created_at
    }

    SYSTEM_COMMAND_RUN {
        bigint id PK
        bigint initiated_by_id FK
        string command_code
        string environment
        string status
        text output
        text error_output
        datetime started_at
        datetime finished_at
    }

    AUTH_USER ||--o| ADMIN_PROFILE : has
    AUTH_USER ||--o{ AUTH_USER_GROUPS : member
    AUTH_GROUP ||--o{ AUTH_USER_GROUPS : includes
    AUTH_GROUP ||--o{ AUTH_GROUP_PERMISSIONS : grants
    AUTH_PERMISSION ||--o{ AUTH_GROUP_PERMISSIONS : assigned
    CONTENT_TYPE ||--o{ AUTH_PERMISSION : describes

    CATEGORY ||--o{ PRODUCT : categorizes
    BRAND o|--o{ PRODUCT : brands
    OPTION_TYPE ||--o{ OPTION_VALUE : defines
    PRODUCT ||--o{ PRODUCT_OPTION_GROUP : configures
    OPTION_TYPE ||--o{ PRODUCT_OPTION_GROUP : used_by
    PRODUCT_OPTION_GROUP ||--o{ PRODUCT_OPTION_VALUE : offers
    OPTION_VALUE ||--o{ PRODUCT_OPTION_VALUE : available_value
    PRODUCT ||--o{ PRODUCT_OPTION_PRICE : has_prices
    OPTION_VALUE ||--o{ PRODUCT_OPTION_PRICE : piece_count_price

    AUTH_USER o|--o| CART : owns
    CART ||--o{ CART_ITEM : contains
    PRODUCT ||--o{ CART_ITEM : selected
    CART_ITEM ||--o{ CART_ITEM_OPTION : stores
    OPTION_TYPE ||--o{ CART_ITEM_OPTION : selected_type
    OPTION_VALUE ||--o{ CART_ITEM_OPTION : selected_value

    AUTH_USER o|--o{ CUSTOMER_ORDER : places
    CUSTOMER_ORDER ||--|{ ORDER_ITEM : contains
    PRODUCT ||--o{ ORDER_ITEM : referenced_by
    ORDER_ITEM ||--o{ ORDER_ITEM_OPTION : snapshots
    CUSTOMER_ORDER ||--o| PAYMENT : paid_by
    AUTH_USER ||--o{ REVIEW : writes
    PRODUCT ||--o{ REVIEW : receives

    PRODUCT ||--o{ STOCK_MOVEMENT : has
    CUSTOMER_ORDER o|--o{ STOCK_MOVEMENT : reference
    FOOTER_SECTION ||--o{ FOOTER_LINK : contains
    CUSTOMER_ORDER o|--o{ META_EVENT_LOG : attributed_to

    AUTH_USER o|--o{ CATEGORY : deleted_by
    AUTH_USER o|--o{ PRODUCT : deleted_by
    AUTH_USER o|--o{ BRAND : deleted_by
    AUTH_USER o|--o{ REVIEW : deleted_by

    AUTH_USER o|--o{ AUDIT_LOG : actor
    AUTH_USER o|--o{ BULK_ACTION_BATCH : initiates
    AUTH_USER o|--o{ SYSTEM_COMMAND_RUN : initiates
```

## 3. Entity Groups and Relationships

### 3.1 Identity and Admin RBAC

-   `AUTH_USER`: Django's built-in user table for customers and admins.
-   `ADMIN_PROFILE`: Optional admin-only profile details, one-to-one
    with User.
-   `AUTH_GROUP`: Django's built-in Group table.
    `django-role-permissions` maps each code-defined role to a Group.
-   `AUTH_PERMISSION`: Django's built-in Permission table. Permission
    codenames are declared by each role's `available_permissions`.
-   `AUTH_USER_GROUPS`: Django's built-in many-to-many table assigning
    users to groups/roles.
-   `AUTH_GROUP_PERMISSIONS`: Django's built-in many-to-many table
    assigning permissions to groups.
-   `CONTENT_TYPE`: Django's built-in model registry referenced by
    `AUTH_PERMISSION`.

Role classes live in a Python `roles.py` module using
`AbstractUserRole`; configure `ROLEPERMISSIONS_MODULE` accordingly.
`sync_roles` synchronizes the code-defined roles/permissions with Django
Groups/Permissions. There are no separate custom `ADMIN_ROLE`,
`ADMIN_PERMISSION`, `ADMIN_USER_ROLE` or `ADMIN_ROLE_PERMISSION`
business tables.

`is_staff=True` gates access to Django Admin. Use package `has_role()` /
`has_permission()` checks for custom dashboard actions.
`is_superuser=True` is the full-access account. Do not create a
duplicate authentication/password table.

### 3.2 Category, Brand and Product

-   One Category can contain many Products.
-   One Brand can be associated with many Products; Brand is optional on
    Product.
-   Category and Product use `HasSEO` and `SoftDeleteModel`.
-   Brand may use `SoftDeleteModel`.
-   Product has `product_type=SIMPLE` or `OPTION_WISE`.
-   Product stock is stored once on Product and shared across option
    selections.

### 3.3 Product Options and Pricing

-   `OPTION_TYPE` defines Color, Size, Weight and Piece Count.
-   `OPTION_VALUE` stores values such as Red, Black, M, L, XL, 5g, 10g,
    1 Piece and 2 Pieces.
-   `PRODUCT_OPTION_GROUP` enables an option type for a product and sets
    required/optional.
-   `PRODUCT_OPTION_VALUE` maps the values available to that product.
-   `PRODUCT_OPTION_PRICE` stores one price for each product/Piece Count
    value.

**Version 1 rule:** Only Piece Count changes price. Color, Size and
Weight are optional descriptive selections. There is no
combination-specific SKU or stock table.

### 3.4 Guest and Registered Carts

-   A Cart belongs either to a registered User or to a guest
    `session_key`.
-   A Cart must not have both owner types at once.
-   A Cart contains multiple Cart Items.
-   Cart Item stores selected values through Cart Item Option rows.
-   Different option configurations can create separate cart lines.
-   A configuration hash identifies an identical product/option
    combination for quantity merging.

### 3.5 Orders and Payments

-   Customer Order has a nullable User FK so a guest can place an order.
-   Every order stores customer name, email, phone and shipping
    snapshots.
-   An Order contains one or more Order Items.
-   Order Item stores product name, SKU, price, quantity, line total and
    option snapshots.
-   Order Item Option stores labels/codes as snapshots so later option
    edits do not rewrite order history.
-   Payment is one-to-one with Order in version 1; it can become
    one-to-many if retries are added later.

### 3.6 Site Settings and Footer

-   `SITE_SETTINGS` is a singleton-style record.
-   `FOOTER_SECTION` stores editable footer columns/groups.
-   `FOOTER_LINK` stores links inside a footer section.
-   Logo/favicon files live in media storage; database stores file
    paths.

### 3.7 Tracking

-   `TRACKING_SETTINGS` stores Pixel ID, enable flags and event
    switches.
-   CAPI access token is stored in server environment, not in this
    table.
-   `META_EVENT_LOG` records event ID, event name, delivery status and
    safe response metadata.
-   Browser and server copies of an event use the same event ID for
    deduplication.

### 3.8 Audit, Bulk Actions and System Commands

-   `AUDIT_LOG` is append-only and records
    actor/action/target/before-after metadata.
-   `BULK_ACTION_BATCH` records summary counts/results; individual
    successes also create Audit Log rows.
-   `SYSTEM_COMMAND_RUN` records allowlisted Django management command
    execution.
-   Dashboard, Trash and System Commands are interfaces/workflows, not
    separate database entities.

## 4. Soft Delete Design

The abstract `SoftDeleteModel` provides:

``` text
is_deleted   BOOLEAN   NOT NULL DEFAULT FALSE
deleted_at   DATETIME  NULL
deleted_by   FK        NULL -> AUTH_USER.id (SET_NULL)
```

Use it for Category and Product as mandatory requirements, and for
eligible Brand, Review and OptionType/OptionValue records.

``` mermaid
flowchart TD
    A[Active record] -->|Move to Trash| B[Trashed record]
    B -->|Restore| A
    B -->|Superuser confirms| C[Permanent Delete]
```

-   Normal querysets return `is_deleted=False`.
-   Trash explicitly queries `is_deleted=True`.
-   Restore clears all soft-delete fields.
-   Permanent Delete is superuser-only and must respect FK constraints.
-   Orders, Payments, Audit Logs and System Command Run rows are
    retained.
-   Admin users are deactivated, not deleted.
-   Trashed Products cannot be purchased.
-   Products under trashed/inactive Categories are not publicly
    discoverable.

## 5. HasSEO Design

`HasSEO` is an abstract model used by Category and Product. It adds
these columns to each table and creates no SEO table:

``` text
has_seo
meta_title
meta_description
meta_keywords
canonical_url
og_title
og_description
og_image
robots_index
robots_follow
```

## 6. Important FK and Delete Behaviors

  -----------------------------------------------------------------------
  Relationship            Recommended Django      Reason
                          `on_delete`             
  ----------------------- ----------------------- -----------------------
  Product → Category      `PROTECT`               Prevent deleting
                                                  category while products
                                                  reference it

  Product → Brand         `SET_NULL` or `PROTECT` Preserve product if
                                                  brand is removed

  ProductOptionGroup →    `CASCADE`               Product option
  Product                                         configuration depends
                                                  on product

  ProductOptionGroup →    `PROTECT`               Protect option
  OptionType                                      definitions in use

  ProductOptionValue →    `PROTECT`               Protect configured
  OptionValue                                     option values

  ProductOptionPrice →    `PROTECT`               Preserve option-wise
  Piece Count value                               price mapping

  Cart → User             `CASCADE`               Cart is temporary;
                                                  normal account flow
                                                  deactivates users

  CartItem → Cart         `CASCADE`               Cart item depends on
                                                  cart

  CartItem → Product      `PROTECT` or controlled Avoid invalid cart
                          cleanup                 references

  CustomerOrder → User    `SET_NULL`              Preserve guest/order
                                                  history

  OrderItem →             `PROTECT`               Preserve order history
  CustomerOrder                                   

  OrderItem → Product     `PROTECT`               Preserve historical
                                                  product reference

  Payment → CustomerOrder `PROTECT`               Preserve payment
                                                  history

  Review → Product        `PROTECT`               Resolve reviews before
                                                  permanent product
                                                  deletion

  Deleted By → User       `SET_NULL`              Preserve trashed record

  Audit Log actor → User  `SET_NULL`              Preserve audit history

  System Command actor →  `SET_NULL`              Preserve command
  User                                            history

  FooterLink →            `CASCADE`               Link depends on section
  FooterSection                                   
  -----------------------------------------------------------------------

Never cascade-delete Order, Order Item or Payment history from Product
or User.

## 7. Entities Not Represented as Separate Tables

-   `SoftDeleteModel` and `HasSEO` are abstract Django models.
-   Trash is a filtered view over soft-deleted rows.
-   Dashboard is an interface, not a database table.
-   Product option combinations are not separate ProductVariant rows in
    version 1.
-   Django authentication tables are managed by Django migrations.
-   Uploaded images are stored in media storage; database stores file
    paths.
-   Meta CAPI token is stored in server environment configuration, not
    in a normal database column.

## 8. Design Assumptions

1.  One active cart per registered customer; guest carts use session
    keys.
2.  A cart line is distinguished by its selected option configuration.
3.  One selected value per option type per cart/order line.
4.  Piece Count is required for option-wise products.
5.  Only Piece Count affects price in version 1.
6.  Product stock is shared across options.
7.  One Payment per Order in the first release.
8.  Admin roles/permissions are custom RBAC; Django User remains
    identity source.
9.  Guest order lookup requires verification.
10. Audit Logs and System Command history are retained.

## 9. Implementation Order

1.  `core`: SoftDeleteModel, HasSEO and managers.
2.  `categories`: Category.
3.  `products`: Brand, Product, OptionType, OptionValue,
    ProductOptionGroup, ProductOptionValue, ProductOptionPrice and
    StockMovement.
4.  `accounts` and `cart`: profile as needed, Cart, CartItem and
    CartItemOption.
5.  `orders` and `payments`: CustomerOrder, OrderItem, OrderItemOption
    and Payment.
6.  `reviews`: Review.
7.  `dashboard`: Integrate django-role-permissions with Django
    Groups/Permissions; create AuditLog, BulkActionBatch and
    SystemCommandRun.
8.  `site_settings`: SiteSettings, FooterSection and FooterLink.
9.  `tracking`: TrackingSettings and MetaEventLog.

Run migrations and tests after each model group.

## 10. Package and File Storage Notes

-   `django-role-permissions` does not require duplicate role/permission
    business tables. It uses Django's Groups and Permissions and
    code-defined role classes.
-   `django-jazzmin` themes Django Admin and creates no database tables.
-   Django `FileField`/`ImageField` columns store file names/paths; file
    bytes are managed by Django storage under `MEDIA_ROOT` or another
    configured storage backend.
-   `ImageField` is used for images; generic `FileField` is used for
    documents such as product datasheets.
-   Product `document_path`, product `image_path`, site logo/favicon and
    SEO image paths are represented as file path attributes in this ERD.
