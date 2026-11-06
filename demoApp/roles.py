from typing import ClassVar

from rolepermissions.roles import AbstractUserRole


class StoreManager(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {
        "category_view": True,
        "category_create": True,
        "category_update": True,
        "category_trash": True,
        "category_restore": True,
        "category_force_delete": False,
        "product_view": True,
        "product_create": True,
        "product_update": True,
        "product_trash": True,
        "product_restore": True,
        "product_force_delete": False,
        "order_view": True,
        "order_update_status": True,
        "payment_view": True,
        "payment_update_status": True,
        "review_view": True,
        "review_moderate": True,
        "review_trash": True,
        "review_restore": True,
        "review_force_delete": False,
        "customer_view": True,
        "dashboard_view": True,
        "bulk_action_execute": True,
    }


class ProductManager(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {
        "category_view": True,
        "category_create": True,
        "category_update": True,
        "category_trash": True,
        "category_restore": True,
        "category_force_delete": False,
        "product_view": True,
        "product_create": True,
        "product_update": True,
        "product_trash": True,
        "product_restore": True,
        "product_force_delete": False,
        "bulk_action_execute": True,
    }


class OrderManager(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {
        "order_view": True,
        "order_update_status": True,
        "payment_view": True,
        "payment_update_status": True,
        "customer_view": True,
        "dashboard_view": True,
        "bulk_action_execute": True,
    }


class ReviewManager(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {
        "review_view": True,
        "review_moderate": True,
        "review_trash": True,
        "review_restore": True,
        "review_force_delete": False,
        "dashboard_view": True,
        "bulk_action_execute": True,
    }


class SupportManager(AbstractUserRole):
    available_permissions: ClassVar[dict[str, bool]] = {
        "customer_view": True,
        "order_view": True,
        "dashboard_view": True,
    }