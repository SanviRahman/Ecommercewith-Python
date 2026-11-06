from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Category


class CategoryModelTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="qa_admin",
            password="test-password"
        )

    def create_category(self, slug="electronics"):
        return Category.objects.create(name="Electronics", slug=slug)

    def test_category_creation(self):
        category = self.create_category()

        self.assertEqual(category.name, "Electronics")
        self.assertFalse(category.is_deleted)
        self.assertFalse(category.has_seo)
        self.assertIsNotNone(category.created_at)
        self.assertIsNotNone(category.updated_at)

    def test_soft_delete_moves_category_to_trash(self):
        category = self.create_category()

        self.assertTrue(category.soft_delete(user=self.user))

        trashed = Category.deleted_objects.get(pk=category.pk)
        self.assertTrue(trashed.is_deleted)
        self.assertEqual(trashed.deleted_by, self.user)
        self.assertIsNotNone(trashed.deleted_at)
        self.assertFalse(Category.objects.filter(pk=category.pk).exists())

    def test_repeated_soft_delete_returns_false(self):
        category = self.create_category()
        category.soft_delete(user=self.user)

        self.assertFalse(category.soft_delete(user=self.user))

    def test_restore_returns_category_to_active_manager(self):
        category = self.create_category()
        category.soft_delete(user=self.user)

        trashed = Category.deleted_objects.get(pk=category.pk)
        self.assertTrue(trashed.restore())

        restored = Category.objects.get(pk=category.pk)
        self.assertFalse(restored.is_deleted)
        self.assertIsNone(restored.deleted_at)
        self.assertIsNone(restored.deleted_by)

    def test_restore_active_category_returns_false(self):
        category = self.create_category()

        self.assertFalse(category.restore())

    def test_managers_separate_active_and_trashed_categories(self):
        active = self.create_category()
        trashed = self.create_category(slug="computers")
        trashed.soft_delete(user=self.user)

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.deleted_objects.count(), 1)
        self.assertEqual(Category.all_objects.count(), 2)
        self.assertTrue(Category.objects.filter(pk=active.pk).exists())

    def test_queryset_delete_uses_soft_delete(self):
        category = self.create_category()

        deleted_count, _ = Category.objects.filter(pk=category.pk).delete()

        self.assertEqual(deleted_count, 1)
        self.assertTrue(Category.deleted_objects.filter(pk=category.pk).exists())

    def test_queryset_restore(self):
        category = self.create_category()
        category.soft_delete(user=self.user)

        restored_count = Category.deleted_objects.filter(pk=category.pk).restore()

        self.assertEqual(restored_count, 1)
        self.assertTrue(Category.objects.filter(pk=category.pk).exists())

    def test_hard_delete_permanently_removes_category(self):
        category = self.create_category()
        category.soft_delete(user=self.user)

        category.hard_delete()

        self.assertFalse(Category.all_objects.filter(pk=category.pk).exists())

    def test_seo_fields_exist(self):
        fields = [
            "has_seo",
            "meta_title",
            "meta_description",
            "meta_keywords",
            "canonical_url",
            "og_title",
            "og_description",
            "og_image",
            "robots_index",
            "robots_follow",
        ]

        for field in fields:
            with self.subTest(field=field):
                self.assertIsNotNone(Category._meta.get_field(field))
