from django.conf import settings
from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):

    def soft_delete(self, user=None):
        now = timezone.now()
        return self.filter(is_deleted=False).update(is_deleted=True, deleted_at=now, deleted_by=user, updated_at=now)

    def restore(self):
        now = timezone.now()
        return self.filter(is_deleted=True).update(is_deleted=False, deleted_at=None, deleted_by=None, updated_at=now)

    def hard_delete(self):
        return super().delete()

    def delete(self):
        count = self.soft_delete()
        return count, {self.model._meta.label: count} if count else {}


class SoftDeleteManager(models.Manager.from_queryset(SoftDeleteQuerySet)):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)


class DeletedObjectsManager(models.Manager.from_queryset(SoftDeleteQuerySet)):

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=True)


class SoftDeleteModel(TimeStampedModel):
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="+")

    objects = SoftDeleteManager()
    all_objects = SoftDeleteQuerySet.as_manager()
    deleted_objects = DeletedObjectsManager()

    def soft_delete(self, user=None, using=None):
        if self.is_deleted:
            return False

        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.deleted_by = user
        self.save(using=using, update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])
        return True

    def restore(self, using=None):
        if not self.is_deleted:
            return False

        self.is_deleted = False
        self.deleted_at = None
        self.deleted_by = None
        self.save(using=using, update_fields=["is_deleted", "deleted_at", "deleted_by", "updated_at"])
        return True

    def hard_delete(self, using=None, keep_parents=False):
        return super().delete(using=using, keep_parents=keep_parents)

    def delete(self, using=None, keep_parents=False):
        if self.soft_delete(using=using):
            return 1, {self._meta.label: 1}
        return 0, {}

    class Meta:
        abstract = True
        default_manager_name = "objects"
        base_manager_name = "all_objects"


class HasSEO(models.Model):
    has_seo = models.BooleanField(default=False)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)
    meta_keywords = models.CharField(max_length=500, blank=True)
    canonical_url = models.URLField(max_length=500, blank=True)
    og_title = models.CharField(max_length=255, blank=True)
    og_description = models.TextField(blank=True)
    og_image = models.ImageField(upload_to="seo/og/", blank=True, null=True)
    robots_index = models.BooleanField(default=True)
    robots_follow = models.BooleanField(default=True)

    class Meta:
        abstract = True