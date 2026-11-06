from typing import ClassVar

from django.db import models

from core.models import HasSEO, SoftDeleteModel


class Category(SoftDeleteModel, HasSEO):
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=180, unique=True)
    description = models.TextField(blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        indexes: ClassVar[list[models.Index]] = [
            models.Index(fields=["is_deleted", "is_active"]),
            models.Index(fields=["sort_order"]),
        ]
        default_manager_name = "objects"
        base_manager_name = "all_objects"

    def __str__(self):
        return self.name