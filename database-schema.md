# Database Schema

## Ecommerce Practice Project --- MySQL 8.4

**Document version:** 1.1\
**Backend:** Django ORM\
**Database engine:** MySQL 8.4 / InnoDB\
**Source:** Updated Project Overview, PRD and ERD

------------------------------------------------------------------------

## 1. Purpose and Conventions

This document defines the proposed database tables, columns, Django
field types, constraints, indexes and delete behavior. It is a design
blueprint, not an SQL dump. Django migrations create the physical MySQL
schema.

### Conventions

-   Primary keys: `BigAutoField`, unless a Django framework table
    dictates otherwise.
-   Timestamps: timezone-aware `DateTimeField`.
-   Money: `DecimalField(max_digits=12, decimal_places=2)`; never
    `FloatField`.
-   Structured metadata: `JSONField`.
-   Uploaded files: `ImageField`/`FileField` stores a relative file
    path, not image bytes in MySQL.
-   Use explicit foreign-key `on_delete` behavior.
-   Table names below use recommended Django naming (`app_model`).
-   Add `created_at` and `updated_at` to mutable business records where
    appropriate.

## 2. Shared Abstract Models

These abstract Django models do not create their own database tables.

### 2.1 `SoftDeleteModel`

Use for Category and Product as mandatory requirements, and for eligible
Brand, OptionType, OptionValue and Review records. Role
definitions/permissions are code-managed through django-role-permissions
and Django's built-in auth tables, not custom soft-deletable RBAC
tables.

  ------------------------------------------------------------------------
  Field             Django type        Null/default      Purpose
  ----------------- ------------------ ----------------- -----------------
  `is_deleted`      BooleanField       False             Whether record is
                                                         in Trash

  `deleted_at`      DateTimeField      null/blank        When record was
                                                         trashed

  `deleted_by`      ForeignKey(User)   null, `SET_NULL`  Admin who moved
                                                         it to Trash
  ------------------------------------------------------------------------

Recommended managers: - `objects`: active/non-deleted rows only. -
`all_objects`: all rows including Trash. - `deleted_objects`: trashed
rows only.

Normal public/admin querysets must not accidentally include trashed
records.

### 2.2 `HasSEO`

Use for Category and Product. This is an abstract model/mixin, not a
separate table.

  -----------------------------------------------------------------------
  Field                Django type      Null/default     Purpose
  -------------------- ---------------- ---------------- ----------------
  `has_seo`            BooleanField     False            Enable custom
                                                         SEO metadata

  `meta_title`         CharField(255)   blank            Search title

  `meta_description`   TextField or     blank            Search
                       CharField(320)                    description

  `meta_keywords`      CharField(500)   blank            Optional keyword
                                                         field

  `canonical_url`      URLField(500)    blank            Canonical URL

  `og_title`           CharField(255)   blank            Open Graph title

  `og_description`     TextField        blank            Open Graph
                                                         description

  `og_image`           ImageField       blank/null       Social share
                                                         image path

  `robots_index`       BooleanField     True             Allow indexing

  `robots_follow`      BooleanField     True             Allow link
                                                         following
  -----------------------------------------------------------------------

When `has_seo=False`, frontend can use site-level default metadata.

------------------------------------------------------------------------

## 3. Identity and Admin Access Tables

### 3.1 `auth_user` --- Django built-in User

Use Django's built-in authentication model; do not create a duplicate
Admin/User password table.

Important fields include:

  Field            Django type              Purpose
  ---------------- ------------------------ ----------------------------
  `id`             AutoField/BigAutoField   Primary key
  `username`       CharField, unique        Login username
  `email`          EmailField               Email
  `password`       CharField                Django-hashed password
  `is_active`      BooleanField             Active/deactivated account
  `is_staff`       BooleanField             Admin-area access gate
  `is_superuser`   BooleanField             Full Django superuser flag
  `last_login`     DateTimeField            Last login
  `date_joined`    DateTimeField            Registration date

### 3.2 `dashboard_adminprofile`

Optional extra details for admin accounts. Authentication remains in
`auth_user`.

  Field           Django type           Constraint/default
  --------------- --------------------- -----------------------------
  `id`            BigAutoField          PK
  `user`          OneToOneField(User)   Required, unique, `CASCADE`
  `phone`         CharField(30)         blank
  `designation`   CharField(100)        blank
  `avatar`        ImageField            blank
  `created_at`    DateTimeField         auto
  `updated_at`    DateTimeField         auto

### 3.3 `auth_group` --- Django Group / role storage

`django-role-permissions` maps each Python role class to a Django Group.

  Field    Django type              Constraint/default
  -------- ------------------------ ------------------------
  `id`     AutoField/BigAutoField   PK
  `name`   CharField(150)           Unique group/role name

Role names are declared in `roles.py` using `AbstractUserRole`. They are
not created as arbitrary dynamic model rows. Use the package's
`sync_roles` management command after changing role definitions.

### 3.4 `auth_permission` --- Django Permission storage

  Field            Django type              Constraint/default
  ---------------- ------------------------ ---------------------------
  `id`             AutoField/BigAutoField   PK
  `name`           CharField(255)           Human-readable permission
  `content_type`   FK(ContentType)          Required, `CASCADE`
  `codename`       CharField(100)           Permission code

Unique constraint: `(content_type, codename)`.

Permission codenames are declared in each role's
`available_permissions`. The package synchronizes them to Django's
permission table.

### 3.5 `auth_user_groups` --- user-to-role assignment

Django's automatically generated many-to-many table between User and
Group.

  Field        Django type              Constraint/default
  ------------ ------------------------ ---------------------
  `id`         AutoField/BigAutoField   PK
  `user_id`    FK(User)                 Required, `CASCADE`
  `group_id`   FK(Group)                Required, `CASCADE`

Unique constraint: `(user_id, group_id)`.

Use `assign_role()` / `remove_role()` from `rolepermissions.roles`
rather than writing this join table directly.

### 3.6 `auth_group_permissions` --- role-to-permission assignment

Django's automatically generated many-to-many table between Group and
Permission.

  Field             Django type              Constraint/default
  ----------------- ------------------------ ---------------------
  `id`              AutoField/BigAutoField   PK
  `group_id`        FK(Group)                Required, `CASCADE`
  `permission_id`   FK(Permission)           Required, `CASCADE`

Unique constraint: `(group_id, permission_id)`.

These are Django framework-managed tables. Do not create custom
`dashboard_adminrole`, `dashboard_adminpermission`,
`dashboard_adminuserrole` or `dashboard_adminrolepermission` tables.

## 4. Category, Brand and Product Tables

### 4.1 `categories_category`

Includes `SoftDeleteModel` and `HasSEO`.

  Field                Django type            Constraint/default
  -------------------- ---------------------- --------------------
  `id`                 BigAutoField           PK
  `name`               CharField(160)         Required
  `slug`               SlugField(180)         Unique
  `description`        TextField              blank
  `sort_order`         PositiveIntegerField   0
  `is_active`          BooleanField           True
  `is_deleted`         BooleanField           False
  `deleted_at`         DateTimeField          null/blank
  `deleted_by`         FK(User)               null, `SET_NULL`
  `has_seo`            BooleanField           False
  `meta_title`         CharField(255)         blank
  `meta_description`   TextField              blank
  `meta_keywords`      CharField(500)         blank
  `canonical_url`      URLField(500)          blank
  `og_title`           CharField(255)         blank
  `og_description`     TextField              blank
  `og_image`           ImageField             blank/null
  `robots_index`       BooleanField           True
  `robots_follow`      BooleanField           True
  `created_at`         DateTimeField          auto
  `updated_at`         DateTimeField          auto

Indexes: `(is_deleted, is_active)`, `sort_order`; unique `slug`.

`deleted_by` uses `SET_NULL`. Product.category uses `PROTECT`.

### 4.2 `products_brand`

  Field           Django type      Constraint/default
  --------------- ---------------- --------------------
  `id`            BigAutoField     PK
  `name`          CharField(150)   Required
  `slug`          SlugField(170)   Unique
  `description`   TextField        blank
  `logo`          ImageField       blank/null
  `is_active`     BooleanField     True
  `is_deleted`    BooleanField     False
  `deleted_at`    DateTimeField    null/blank
  `deleted_by`    FK(User)         null, `SET_NULL`
  `created_at`    DateTimeField    auto
  `updated_at`    DateTimeField    auto

A Brand referenced by Products cannot be permanently deleted until
references are resolved.

### 4.3 `products_product`

Includes `SoftDeleteModel` and `HasSEO`.

  -----------------------------------------------------------------------
  Field                   Django type             Constraint/default
  ----------------------- ----------------------- -----------------------
  `id`                    BigAutoField            PK

  `category`              FK(Category)            Required, `PROTECT`

  `brand`                 FK(Brand)               null/blank; `SET_NULL`
                                                  or `PROTECT` by policy

  `sku`                   CharField(80)           Unique

  `name`                  CharField(220)          Required

  `slug`                  SlugField(240)          Unique

  `product_type`          CharField(20)           SIMPLE or OPTION_WISE

  `description`           TextField               blank

  `base_price`            DecimalField(12,2)      Required for SIMPLE;
                                                  nullable for
                                                  OPTION_WISE

  `compare_at_price`      DecimalField(12,2)      null/blank

  `stock_quantity`        PositiveIntegerField    0; shared product stock

  `image`                 ImageField              blank/null

  `is_active`             BooleanField            True

  `is_featured`           BooleanField            False

  `is_deleted`            BooleanField            False

  `deleted_at`            DateTimeField           null/blank

  `deleted_by`            FK(User)                null, `SET_NULL`

  `has_seo`               BooleanField            False

  `meta_title`            CharField(255)          blank

  `meta_description`      TextField               blank

  `meta_keywords`         CharField(500)          blank

  `canonical_url`         URLField(500)           blank

  `og_title`              CharField(255)          blank

  `og_description`        TextField               blank

  `og_image`              ImageField              blank/null

  `robots_index`          BooleanField            True

  `robots_follow`         BooleanField            True

  `created_at`            DateTimeField           auto

  `updated_at`            DateTimeField           auto
  -----------------------------------------------------------------------

Indexes: `(category, is_deleted, is_active)`, `(brand, is_deleted)`,
`(product_type, is_active)`, `is_featured`; unique `sku` and `slug`.

Additional optional upload field: - `document` ---
`FileField(upload_to="products/documents/%Y/%m/", blank=True)` for a
product datasheet/manual PDF. This is a generic file path, not image
data. Product photos continue to use `ImageField`.

Business constraints: - SIMPLE product requires `base_price`. -
OPTION_WISE product requires a Piece Count group and active
ProductOptionPrice rows. - OPTION_WISE displayed price/range is derived
from active ProductOptionPrice rows. - Stock is shared across all option
selections. - Product referenced by OrderItem cannot be permanently
deleted.

------------------------------------------------------------------------

## 5. Product Option and Option-wise Pricing Tables

### 5.1 `products_optiontype`

Global option definitions: Color, Size, Weight and Piece Count.

  Field                      Django type            Constraint/default
  -------------------------- ---------------------- --------------------------------
  `id`                       BigAutoField           PK
  `name`                     CharField(80)          Required
  `code`                     SlugField(80)          Unique
  `affects_price`            BooleanField           False except Piece Count in v1
  `is_required_by_default`   BooleanField           False; Piece Count True
  `sort_order`               PositiveIntegerField   0
  `is_active`                BooleanField           True
  `is_deleted`               BooleanField           False
  `deleted_at`               DateTimeField          null/blank
  `deleted_by`               FK(User)               null, `SET_NULL`
  `created_at`               DateTimeField          auto
  `updated_at`               DateTimeField          auto

Seed definitions: - Color: optional, does not affect price. - Size:
optional, does not affect price. - Weight: optional, does not affect
price. - Piece Count: required for option-wise products and affects
price.

### 5.2 `products_optionvalue`

  Field             Django type            Constraint/default
  ----------------- ---------------------- ----------------------------
  `id`              BigAutoField           PK
  `option_type`     FK(OptionType)         Required, `PROTECT`
  `display_label`   CharField(100)         Required
  `unique_code`     SlugField(100)         Required
  `swatch_hex`      CharField(7)           blank/null; e.g. `#C63A3A`
  `sort_order`      PositiveIntegerField   0
  `is_active`       BooleanField           True
  `is_deleted`      BooleanField           False
  `deleted_at`      DateTimeField          null/blank
  `deleted_by`      FK(User)               null, `SET_NULL`
  `created_at`      DateTimeField          auto
  `updated_at`      DateTimeField          auto

Constraint: unique `(option_type, unique_code)`.

Example values: Red, Black; M, L, XL; 5g, 10g; 1 Piece, 2 Pieces, 3
Pieces.

Do not permanently delete an OptionValue while ProductOptionValue or
ProductOptionPrice rows reference it.

### 5.3 `products_productoptiongroup`

Enables an option type for one product.

  Field           Django type            Constraint/default
  --------------- ---------------------- ---------------------
  `id`            BigAutoField           PK
  `product`       FK(Product)            Required, `CASCADE`
  `option_type`   FK(OptionType)         Required, `PROTECT`
  `is_required`   BooleanField           Per-product setting
  `sort_order`    PositiveIntegerField   0
  `created_at`    DateTimeField          auto

Constraint: unique `(product, option_type)`.

For OPTION_WISE products, Piece Count group must exist and be required.
Color/Size/Weight groups are optional.

### 5.4 `products_productoptionvalue`

Maps values available for a product option group.

  -------------------------------------------------------------------------
  Field                    Django type              Constraint/default
  ------------------------ ------------------------ -----------------------
  `id`                     BigAutoField             PK

  `product_option_group`   FK(ProductOptionGroup)   Required, `CASCADE`

  `option_value`           FK(OptionValue)          Required, `PROTECT`

  `sort_order`             PositiveIntegerField     0
  -------------------------------------------------------------------------

Constraint: unique `(product_option_group, option_value)`.

Validate that OptionValue belongs to the same OptionType as
ProductOptionGroup.

### 5.5 `products_productoptionprice`

Stores the price for each Piece Count value on a product.

  Field                 Django type          Constraint/default
  --------------------- -------------------- ---------------------
  `id`                  BigAutoField         PK
  `product`             FK(Product)          Required, `CASCADE`
  `piece_count_value`   FK(OptionValue)      Required, `PROTECT`
  `price`               DecimalField(12,2)   Required
  `compare_at_price`    DecimalField(12,2)   null/blank
  `is_active`           BooleanField         True
  `created_at`          DateTimeField        auto
  `updated_at`          DateTimeField        auto

Constraint: unique `(product, piece_count_value)`.

Validation: - `piece_count_value.option_type.code` must be
`piece_count`. - Value must be assigned to that product's Piece Count
group. - Only this table determines option-wise price in version 1. -
Color/Size/Weight do not add price rows. - Product stock remains in
`products_product.stock_quantity`.

------------------------------------------------------------------------

## 6. Cart Tables --- Guest and Registered

### 6.1 `cart_cart`

  Field           Django type      Constraint/default
  --------------- ---------------- -----------------------
  `id`            BigAutoField     PK
  `user`          FK(User)         null/blank, `CASCADE`
  `session_key`   CharField(100)   null/blank, unique
  `expires_at`    DateTimeField    null/blank
  `created_at`    DateTimeField    auto
  `updated_at`    DateTimeField    auto

Constraints: - Cart has exactly one owner: `user` XOR `session_key`. -
One active cart per registered user. - One active cart per guest
session. - Enforce with CheckConstraint where supported and
model/service validation.

On login, merge eligible guest cart lines into the customer cart. Merge
identical product/option configurations by adding quantities, then clear
the guest cart.

### 6.2 `cart_cartitem`

  Field                   Django type            Constraint/default
  ----------------------- ---------------------- -------------------------------------------
  `id`                    BigAutoField           PK
  `cart`                  FK(Cart)               Required, `CASCADE`
  `product`               FK(Product)            Required, `PROTECT` or controlled cleanup
  `quantity`              PositiveIntegerField   Greater than 0
  `configuration_hash`    CharField(64)          Required
  `unit_price_snapshot`   DecimalField(12,2)     Required
  `created_at`            DateTimeField          auto
  `updated_at`            DateTimeField          auto

Recommended unique constraint: `(cart, product, configuration_hash)`.

`configuration_hash` is computed server-side from sorted selected option
type/value IDs. Different selections can be separate lines.

### 6.3 `cart_cartitemoption`

  Field            Django type       Constraint/default
  ---------------- ----------------- ---------------------
  `id`             BigAutoField      PK
  `cart_item`      FK(CartItem)      Required, `CASCADE`
  `option_type`    FK(OptionType)    Required, `PROTECT`
  `option_value`   FK(OptionValue)   Required, `PROTECT`

Constraint: unique `(cart_item, option_type)`, meaning one selected
value per option type per cart line.

Validation: - Value must be assigned to the Product's matching option
group. - Optional groups may be omitted. - Piece Count is mandatory for
OPTION_WISE products. - Unit price is calculated from
ProductOptionPrice, never accepted from browser.

------------------------------------------------------------------------

## 7. Orders and Payments

### 7.1 `orders_customerorder`

  -----------------------------------------------------------------------
  Field                         Django type          Constraint/default
  ----------------------------- -------------------- --------------------
  `id`                          BigAutoField         PK

  `user`                        FK(User)             null/blank,
                                                     `SET_NULL`

  `order_number`                CharField(40)        Unique, generated
                                                     server-side

  `customer_name`               CharField(180)       Required snapshot

  `customer_email`              EmailField           Required for guest
                                                     verification

  `customer_phone`              CharField(30)        Required/contact
                                                     snapshot

  `shipping_address`            TextField            Required

  `shipping_area`               CharField(120)       blank

  `shipping_city`               CharField(120)       Required

  `shipping_postal_code`        CharField(20)        blank

  `customer_note`               TextField            blank

  `total_amount`                DecimalField(12,2)   Server-calculated

  `status`                      CharField(30)        pending, confirmed,
                                                     shipped, delivered,
                                                     cancelled

  `guest_tracking_token_hash`   CharField(128)       null/blank

  `created_at`                  DateTimeField        auto

  `updated_at`                  DateTimeField        auto
  -----------------------------------------------------------------------

Indexes: `(user, created_at)`, `(status, created_at)`, `customer_email`;
unique `order_number`.

Guest orders have `user=NULL` but retain customer/shipping snapshots.
Guest tracking requires order number plus verified email/phone or a
secure token. Do not expose an order by guessable order number alone.

Orders are retained and excluded from Trash/permanent delete.

### 7.2 `orders_orderitem`

  Field                     Django type            Constraint/default
  ------------------------- ---------------------- ---------------------
  `id`                      BigAutoField           PK
  `order`                   FK(CustomerOrder)      Required, `PROTECT`
  `product`                 FK(Product)            Required, `PROTECT`
  `product_name_snapshot`   CharField(220)         Required
  `sku_snapshot`            CharField(80)          blank
  `unit_price_snapshot`     DecimalField(12,2)     Required
  `quantity`                PositiveIntegerField   Greater than 0
  `line_total`              DecimalField(12,2)     Server-calculated

Indexes: `order`, `product`.

Do not calculate historical order totals from current Product price.

### 7.3 `orders_orderitemoption`

  Field                           Django type          Constraint/default
  ------------------------------- -------------------- ---------------------
  `id`                            BigAutoField         PK
  `order_item`                    FK(OrderItem)        Required, `CASCADE`
  `option_type_name_snapshot`     CharField(80)        Required
  `option_value_label_snapshot`   CharField(100)       Required
  `option_value_code_snapshot`    CharField(100)       blank
  `price_effect_snapshot`         DecimalField(12,2)   default 0

Store snapshots rather than relying only on live OptionValue FKs.
Historical orders remain readable if option labels change.

### 7.4 `payments_payment`

  Field                     Django type                    Constraint/default
  ------------------------- ------------------------------ ---------------------------------
  `id`                      BigAutoField                   PK
  `order`                   OneToOneField(CustomerOrder)   Required, `PROTECT`
  `payment_method`          CharField(40)                  COD or MOCK in version 1
  `amount`                  DecimalField(12,2)             Required
  `transaction_reference`   CharField(160)                 blank
  `status`                  CharField(30)                  pending, paid, failed, refunded
  `provider_response`       JSONField                      null/blank; sanitized only
  `paid_at`                 DateTimeField                  null/blank
  `created_at`              DateTimeField                  auto
  `updated_at`              DateTimeField                  auto

One Payment per Order in version 1. If payment retries are added later,
replace OneToOne with ForeignKey and add an attempt number.

Never store card number, CVV or raw payment credentials. Payments are
retained and excluded from normal Trash/permanent delete.

------------------------------------------------------------------------

## 8. Reviews and Stock Movement

### 8.1 `reviews_review`

  Field           Django type                 Constraint/default
  --------------- --------------------------- ---------------------
  `id`            BigAutoField                PK
  `user`          FK(User)                    Required
  `product`       FK(Product)                 Required, `PROTECT`
  `rating`        PositiveSmallIntegerField   Validate 1--5
  `comment`       TextField                   blank
  `is_approved`   BooleanField                moderation policy
  `is_deleted`    BooleanField                False
  `deleted_at`    DateTimeField               null/blank
  `deleted_by`    FK(User)                    null, `SET_NULL`
  `created_at`    DateTimeField               auto
  `updated_at`    DateTimeField               auto

Recommended unique constraint: `(user, product)` if one review per
customer/product. Trashed reviews are hidden publicly.

### 8.2 `products_stockmovement`

  Field              Django type            Constraint/default
  ------------------ ---------------------- ------------------------------------
  `id`               BigAutoField           PK
  `product`          FK(Product)            Required, `PROTECT`
  `order`            FK(CustomerOrder)      null/blank, `SET_NULL`
  `performed_by`     FK(User)               null, `SET_NULL`
  `movement_type`    CharField(30)          purchase, sale, return, adjustment
  `quantity_delta`   IntegerField           Signed stock change
  `stock_before`     PositiveIntegerField   Required
  `stock_after`      PositiveIntegerField   Required
  `reason`           CharField(255)         blank
  `created_at`       DateTimeField          auto

Update Product stock and insert StockMovement in one transaction.

------------------------------------------------------------------------

## 9. Site Settings and Footer Tables

### 9.1 `site_settings_sitesettings`

Singleton-style settings row. Enforce a single active settings record in
application/admin logic.

  Field                        Django type            Constraint/default
  ---------------------------- ---------------------- --------------------------
  `id`                         BigAutoField           PK; singleton convention
  `site_name`                  CharField(160)         Required
  `tagline`                    CharField(255)         blank
  `logo`                       ImageField             blank/null
  `favicon`                    ImageField/FileField   blank/null
  `contact_email`              EmailField             blank
  `contact_phone`              CharField(40)          blank
  `contact_address`            TextField              blank
  `footer_about`               TextField              blank
  `footer_email`               EmailField             blank
  `footer_phone`               CharField(40)          blank
  `footer_address`             TextField              blank
  `footer_copyright`           CharField(255)         blank
  `social_links`               JSONField              empty list/object
  `default_meta_title`         CharField(255)         blank
  `default_meta_description`   TextField              blank
  `default_og_image`           ImageField             blank/null
  `updated_by`                 FK(User)               null, `SET_NULL`
  `created_at`                 DateTimeField          auto
  `updated_at`                 DateTimeField          auto

Logo/favicon files are stored in media storage; MySQL stores file paths.
CAPI token must not be stored here.

### 9.2 `site_settings_footersection`

  Field          Django type            Constraint/default
  -------------- ---------------------- --------------------
  `id`           BigAutoField           PK
  `title`        CharField(120)         Required
  `sort_order`   PositiveIntegerField   0
  `is_active`    BooleanField           True
  `created_at`   DateTimeField          auto
  `updated_at`   DateTimeField          auto

### 9.3 `site_settings_footerlink`

  Field          Django type            Constraint/default
  -------------- ---------------------- ---------------------
  `id`           BigAutoField           PK
  `section`      FK(FooterSection)      Required, `CASCADE`
  `label`        CharField(120)         Required
  `url`          CharField(500)         Required
  `target`       CharField(20)          `_self` or `_blank`
  `sort_order`   PositiveIntegerField   0
  `is_active`    BooleanField           True

Index: `(section, is_active, sort_order)`.

------------------------------------------------------------------------

## 10. Meta Pixel and CAPI Tables

### 10.1 `tracking_trackingsettings`

Singleton-style tracking configuration.

  Field                  Django type     Constraint/default
  ---------------------- --------------- --------------------
  `id`                   BigAutoField    PK
  `meta_pixel_id`        CharField(80)   blank
  `pixel_enabled`        BooleanField    False
  `capi_enabled`         BooleanField    False
  `track_page_view`      BooleanField    True
  `track_view_content`   BooleanField    True
  `track_add_to_cart`    BooleanField    True
  `track_checkout`       BooleanField    True
  `track_purchase`       BooleanField    True
  `test_event_code`      CharField(80)   blank; test only
  `updated_by`           FK(User)        null, `SET_NULL`
  `created_at`           DateTimeField   auto
  `updated_at`           DateTimeField   auto

**Secret handling:** `META_CAPI_ACCESS_TOKEN` must come from server
environment variables or secure secret storage. Never expose it in
templates, JavaScript, normal settings forms, Audit Logs or command
output.

### 10.2 `tracking_metaeventlog`

  -----------------------------------------------------------------------
  Field                 Django type                 Constraint/default
  --------------------- --------------------------- ---------------------
  `id`                  BigAutoField                PK

  `event_id`            CharField(100)              Unique deduplication
                                                    ID

  `event_name`          CharField(60)               PageView,
                                                    ViewContent,
                                                    AddToCart,
                                                    InitiateCheckout,
                                                    Purchase

  `order`               FK(CustomerOrder)           null/blank,
                                                    `SET_NULL`

  `event_source_url`    URLField(500)               blank

  `delivery_status`     CharField(30)               pending, sent, failed

  `attempts`            PositiveSmallIntegerField   0

  `http_status`         PositiveSmallIntegerField   null/blank

  `response_summary`    TextField                   sanitized and
                                                    length-limited

  `created_at`          DateTimeField               auto

  `sent_at`             DateTimeField               null/blank
  -----------------------------------------------------------------------

Indexes: `(event_name, created_at)`, `(delivery_status, created_at)`;
unique `event_id`.

Do not store access tokens or unnecessary raw personal data in event
logs. Browser Pixel and server CAPI copies of the same event use the
same `event_id`.

------------------------------------------------------------------------

## 11. Audit, Bulk Action and System Command Tables

### 11.1 `dashboard_auditlog`

Append-only audit history.

  -----------------------------------------------------------------------
  Field                   Django type             Constraint/default
  ----------------------- ----------------------- -----------------------
  `id`                    BigAutoField            PK

  `actor`                 FK(User)                null, `SET_NULL`

  `action`                CharField(80)           create, update, trash,
                                                  restore, force_delete,
                                                  etc.

  `module`                CharField(80)           products, roles,
                                                  settings, etc.

  `target_model`          CharField(120)          app/model label

  `target_object_id`      CharField(80)           String to support
                                                  different PK types

  `object_repr`           CharField(255)          Human-readable label

  `before_data`           JSONField               null/blank

  `after_data`            JSONField               null/blank

  `metadata`              JSONField               null/blank

  `ip_address`            GenericIPAddressField   null/blank

  `user_agent`            TextField               blank

  `request_id`            CharField(100)          blank

  `created_at`            DateTimeField           auto
  -----------------------------------------------------------------------

Indexes: `(module, created_at)`, `(action, created_at)`,
`(target_model, target_object_id)`, `(actor, created_at)`.

Rules: - No edit/delete in normal admin UI. - Redact passwords, CAPI
tokens, secret keys and card data. - Actor uses `SET_NULL` so logs
survive account deactivation/removal.

### 11.2 `dashboard_bulkactionbatch`

Stores summary for multi-record admin operations.

  Field               Django type            Constraint/default
  ------------------- ---------------------- ----------------------------------------
  `id`                BigAutoField           PK
  `initiated_by`      FK(User)               null, `SET_NULL`
  `model_label`       CharField(120)         e.g. products.Product
  `action`            CharField(40)          trash, restore, force_delete, activate
  `requested_count`   PositiveIntegerField   0
  `success_count`     PositiveIntegerField   0
  `skipped_count`     PositiveIntegerField   0
  `failed_count`      PositiveIntegerField   0
  `result_summary`    JSONField              empty object
  `created_at`        DateTimeField          auto

Each successful object operation should also create its own AuditLog
entry. Do not store secrets in result summaries.

### 11.3 `dashboard_systemcommandrun`

Records allowlisted Django management command execution.

  Field            Django type               Constraint/default
  ---------------- ------------------------- --------------------------------------
  `id`             BigAutoField              PK
  `initiated_by`   FK(User)                  null, `SET_NULL`
  `command_code`   CharField(80)             Allowlisted code only
  `arguments`      JSONField                 Validated allowlisted arguments only
  `environment`    CharField(20)             local, staging, production
  `status`         CharField(20)             pending, running, success, failed
  `output`         TextField                 Sanitized/truncated
  `error_output`   TextField                 Sanitized/truncated
  `started_at`     DateTimeField             null/blank
  `finished_at`    DateTimeField             null/blank
  `duration_ms`    PositiveBigIntegerField   null/blank
  `created_at`     DateTimeField             auto

Indexes: `(command_code, created_at)`, `(status, created_at)`,
`(initiated_by, created_at)`.

Execution requirements: - Use `django.core.management.call_command`. -
Allowlist `check`, `showmigrations`, `migrate`, `collectstatic`,
`clearsessions`. - Never accept arbitrary shell input or use
`shell=True`, `exec` or `eval`. - Production `migrate` requires
superuser, confirmation and backup warning. - Destructive DB commands
are disabled in production. - Record each run in AuditLog.

------------------------------------------------------------------------

## 12. Important Constraints and Indexes

### Unique constraints

  Table                    Constraint
  ------------------------ -------------------------------------------------------
  Category                 unique `slug`
  Brand                    unique `slug`
  Product                  unique `sku`, unique `slug`
  OptionType               unique `code`
  OptionValue              unique `(option_type, unique_code)`
  ProductOptionGroup       unique `(product, option_type)`
  ProductOptionValue       unique `(product_option_group, option_value)`
  ProductOptionPrice       unique `(product, piece_count_value)`
  Cart                     unique non-null `user`; unique non-null `session_key`
  CartItem                 unique `(cart, product, configuration_hash)`
  CartItemOption           unique `(cart_item, option_type)`
  CustomerOrder            unique `order_number`
  Payment                  unique `order` in version 1
  Review                   recommended unique `(user, product)`
  auth_group               unique `name`
  auth_permission          unique `(content_type, codename)`
  auth_user_groups         unique `(user_id, group_id)`
  auth_group_permissions   unique `(group_id, permission_id)`
  MetaEventLog             unique `event_id`

### Check/application constraints

-   Cart has `user_id` XOR `session_key`.
-   CartItem quantity is greater than zero.
-   Review rating is 1--5.
-   SIMPLE Product requires `base_price`.
-   OPTION_WISE Product requires a required Piece Count group and valid
    price rows.
-   ProductOptionPrice must reference a Piece Count OptionValue.
-   ProductOptionValue must match the group's OptionType.
-   One selected value per option type per CartItem.
-   Guest Order must have valid contact/shipping details.
-   Permanent Delete validates all dependent relationships.

### Delete behavior summary

  Relationship                             Recommended behavior
  ---------------------------------------- --------------------------------------------
  Product → Category                       `PROTECT`
  Product → Brand                          `SET_NULL` or `PROTECT` by policy
  ProductOptionGroup → Product             `CASCADE`
  ProductOptionGroup → OptionType          `PROTECT`
  ProductOptionValue → OptionValue         `PROTECT`
  ProductOptionPrice → Piece Count value   `PROTECT`
  Cart → User                              `CASCADE`
  CartItem → Cart                          `CASCADE`
  CartItem → Product                       `PROTECT` or controlled stale-cart cleanup
  CustomerOrder → User                     `SET_NULL`
  OrderItem → CustomerOrder                `PROTECT`
  OrderItem → Product                      `PROTECT`
  OrderItemOption → OrderItem              `CASCADE`
  Payment → CustomerOrder                  `PROTECT`
  Review → Product                         `PROTECT`
  Deleted By → User                        `SET_NULL`
  AuditLog actor → User                    `SET_NULL`
  SystemCommandRun actor → User            `SET_NULL`
  FooterLink → FooterSection               `CASCADE`

Never cascade-delete Order, Order Item, Payment or Audit Log history
from Product or User.

------------------------------------------------------------------------

## 13. Query and Visibility Rules

1.  Default managers for soft-deletable models exclude trashed rows.
2.  Public catalogue additionally filters `is_active=True`.
3.  Products under trashed/inactive categories are not publicly
    discoverable.
4.  Cart/checkout rejects inactive or trashed products and option
    values.
5.  Trash explicitly queries `is_deleted=True`.
6.  Restore validates unique slug/code and relationship constraints.
7.  Permanent Delete is superuser-only and available only from Trash.
8.  Admin accounts are deactivated; orders/payments/audit/command
    history are retained.
9.  Bulk actions validate each selected record and record per-object
    results.

## 14. Environment Variables and Secrets

Example local `.env` keys (never commit the file):

``` env
APP_ENV=local
DB_NAME=django_db
DB_USER=django_user
DB_PASSWORD=replace_with_private_password
DB_HOST=127.0.0.1
DB_PORT=3307

DJANGO_SECRET_KEY=replace_with_private_secret
META_CAPI_ACCESS_TOKEN=replace_with_private_meta_token
META_GRAPH_API_VERSION=vXX.X
```

Pixel ID may be managed in Tracking Settings. CAPI access token must
remain server-side in environment configuration/secret storage. Never
print it in System Command output or Audit Logs.

## 15. Migration and Implementation Order

Create and migrate models in small groups:

1.  `core`: abstract SoftDeleteModel, HasSEO and managers (no tables).
2.  `categories`: Category.
3.  `products`: Brand, Product, OptionType, OptionValue,
    ProductOptionGroup, ProductOptionValue, ProductOptionPrice,
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

After each group: - Run `makemigrations` locally. - Review the generated
migration. - Run `migrate` against development MySQL. - Verify
tables/foreign keys in MySQL Workbench. - Add model, permission and
deletion tests before continuing.

Do not create every model in one large migration.

------------------------------------------------------------------------

## 16. Package Integration --- django-role-permissions and Jazzmin

### 16.1 Candidate dependencies

``` text
Django==6.1.3
django-role-permissions==3.2.0
django-jazzmin==3.0.5
Pillow
```

These are candidate versions for the current project target, not a claim
of verified Django 6.1 compatibility. The latest
`django-role-permissions` release found is 3.2.0 from June 2023 and
package activity is dormant. Jazzmin 3.0.5 metadata lists Django
classifiers through 6.0, not 6.1. Run compatibility checks before
production use.

### 16.2 `django-role-permissions` integration

-   Install package name `django-role-permissions`.
-   Add app label `rolepermissions` to `INSTALLED_APPS`.
-   Create `config/roles.py` (or `demoApp/roles.py` if the project
    package remains `demoApp`).
-   Define role classes using `AbstractUserRole`.
-   Set `ROLEPERMISSIONS_MODULE` to the correct Python import path.
-   Define permission codenames in each role's `available_permissions`.
-   Use `assign_role`, `remove_role`, `has_role` and `has_permission`.
-   Run `sync_roles` after role-definition changes.
-   Use Django's `auth_group`, `auth_permission`, `auth_user_groups` and
    `auth_group_permissions` tables. No duplicate custom RBAC tables are
    required.
-   Role definitions are code-managed; the admin UI can assign
    predefined roles but cannot create arbitrary new role classes
    without a code change/deployment.

Example settings pattern (adjust the module path to the actual project
package):

``` python
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    # other Django apps...
    "rolepermissions",
    # project apps...
]

ROLEPERMISSIONS_MODULE = "config.roles"
ROLEPERMISSIONS_REGISTER_ADMIN = True
```

Example role definition:

``` python
from rolepermissions.roles import AbstractUserRole

class ProductManager(AbstractUserRole):
    available_permissions = {
        "product_view": True,
        "product_create": True,
        "product_update": True,
        "product_trash": True,
        "product_restore": True,
        "product_force_delete": False,
    }
```

The package documentation describes roles in a Python module and
provides `sync_roles` to synchronize Django Groups/Permissions. Verify
these APIs against the installed package version before implementing
views.

### 16.3 `django-jazzmin` integration

-   Install package name `django-jazzmin`.
-   Add `"jazzmin"` before `"django.contrib.admin"` in `INSTALLED_APPS`.
-   Configure `JAZZMIN_SETTINGS` and `JAZZMIN_UI_TWEAKS` for site title,
    logo, favicon, menu labels, icons and theme.
-   Jazzmin themes Django's built-in Admin. It does not automatically
    theme custom dashboard views; use Bootstrap 5 templates for those
    pages.
-   Run `collectstatic` and verify Jazzmin static assets on cPanel.

### 16.4 Compatibility test gate

Before treating the packages as production-ready on Django 6.1.3: 1.
Install the candidate package versions in the development virtual
environment. 2. Run `python manage.py check`. 3. Run
`python manage.py migrate` in a disposable development database. 4. Open
Django Admin and verify Jazzmin rendering/static assets. 5. Run
`python manage.py sync_roles`; verify Groups/Permissions were
synchronized. 6. Test role assignment and `has_permission()` checks for
staff and superuser accounts. 7. Test custom dashboard permission denial
(403) for unauthorized users. 8. Run the relevant automated tests before
deploying to cPanel.

Do not downgrade Django automatically. If a compatibility test fails,
choose a supported package/Django version combination deliberately.

------------------------------------------------------------------------

## 17. Django FileField and ImageField Storage

`FileField` and `ImageField` are built into Django; they are not
separate pip packages.

### 17.1 Where to use them

  Data                                    Django field
  --------------------------------------- --------------
  Product main image                      `ImageField`
  Brand logo                              `ImageField`
  Site logo and favicon                   `ImageField`
  Product Open Graph image                `ImageField`
  Optional product datasheet/manual PDF   `FileField`

Example Product fields:

``` python
image = models.ImageField(
    upload_to="products/images/%Y/%m/",
    blank=True,
)
document = models.FileField(
    upload_to="products/documents/%Y/%m/",
    blank=True,
)
```

### 17.2 Settings

Configure:

``` python
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"
```

In production/cPanel, make sure the configured media directory exists
and is writable by the application process. Configure the web server to
serve media safely.

### 17.3 Storage and security rules

-   MySQL stores the file path/name; the uploaded file bytes are handled
    by Django's storage backend.
-   Install Pillow for `ImageField`.
-   Validate file size, allowed extensions and actual file content on
    the server.
-   Use controlled `upload_to` paths and safe generated filenames.
-   Do not trust the browser-provided MIME type or filename.
-   Do not upload executable files into publicly executable directories.
-   Private documents must be served through an authorized view, not a
    public direct URL.
-   Back up media storage separately from the MySQL database.
-   When replacing/removing files, handle old-file cleanup carefully; a
    database rollback does not automatically restore a deleted file.

## 18. Official Package and Framework References

-   Django `FileField` / `ImageField`:
    https://docs.djangoproject.com/en/6.1/ref/models/fields/#filefield
-   Django file uploads and storage:
    https://docs.djangoproject.com/en/6.1/topics/files/
-   `django-role-permissions` installation and role definitions:
    https://django-role-permissions.readthedocs.io/en/stable/
-   `django-role-permissions` PyPI releases:
    https://pypi.org/project/django-role-permissions/
-   Jazzmin installation:
    https://django-jazzmin.readthedocs.io/installation/
-   Jazzmin PyPI releases and Django classifiers:
    https://pypi.org/project/django-jazzmin/
