from django.contrib import admin, messages
from django.contrib.admin import helpers
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from rolepermissions.checkers import has_permission

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "is_deleted", "sort_order", "created_at")
    search_fields = ("name", "slug")
    list_filter = ("is_active", "is_deleted")
    ordering = ("sort_order", "name")
    readonly_fields = ("is_deleted", "deleted_at", "deleted_by", "created_at", "updated_at")
    list_select_related = ("deleted_by",)
    actions = ("move_to_trash", "restore_selected", "permanently_delete_selected")

    def has_module_permission(self, request):
        return any(has_permission(request.user, p) for p in ("category_view", "category_create", "category_update", "category_trash", "category_restore"))

    def has_view_permission(self, request, obj=None):
        return has_permission(request.user, "category_view")

    def has_add_permission(self, request):
        return has_permission(request.user, "category_create")

    def has_change_permission(self, request, obj=None):
        return has_permission(request.user, "category_update")

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        return Category.all_objects.all().order_by(*self.ordering)

    def get_actions(self, request):
        actions = super().get_actions(request)
        if not request.user.is_superuser or request.GET.get("is_deleted__exact") != "1":
            actions.pop("permanently_delete_selected", None)
        return actions

    @admin.action(permissions=["trash"], description="Move selected categories to Trash")
    def move_to_trash(self, request, queryset):
        count = queryset.soft_delete(user=request.user)
        self.message_user(request, f"{count} categories moved to Trash.")

    def has_trash_permission(self, request):
        return has_permission(request.user, "category_trash")

    @admin.action(permissions=["restore"], description="Restore selected categories")
    def restore_selected(self, request, queryset):
        count = queryset.restore()
        self.message_user(request, f"{count} categories restored.")

    def has_restore_permission(self, request):
        return has_permission(request.user, "category_restore")

    @admin.action(permissions=["force_delete"], description="Permanently delete selected trashed categories")
    def permanently_delete_selected(self, request, queryset):
        if not request.user.is_superuser:
            raise PermissionDenied

        queryset = queryset.filter(is_deleted=True)

        if not queryset.exists():
            self.message_user(request, "Select trashed categories only.", level=messages.WARNING)
            return None

        _, _, perms_needed, protected = self.get_deleted_objects(queryset, request)
        perms_needed.discard(self.opts.verbose_name)

        if request.POST.get("post") and not protected and not perms_needed:
            count = queryset.count()
            queryset.hard_delete()
            self.message_user(request, f"{count} categories permanently deleted.", level=messages.SUCCESS)
            return None

        context = {
            **self.admin_site.each_context(request),
            "title": "Confirm Permanent Delete",
            "opts": self.model._meta,
            "queryset": queryset,
            "action_checkbox_name": helpers.ACTION_CHECKBOX_NAME,
            "action_name": "permanently_delete_selected",
            "perms_lacking": perms_needed,
            "protected": protected,
        }

        request.current_app = self.admin_site.name
        return TemplateResponse(request, "admin/categories/category/confirm_permanent_delete.html", context)

    def has_force_delete_permission(self, request):
        return request.user.is_superuser