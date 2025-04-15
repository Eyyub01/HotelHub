from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
import os

from accounts.models import CustomUser

# Tests for CustomUser model:

class CustomUserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'phone_number': '+994123456789',
            'role': CustomUser.CUSTOMER,
            'is_owner_requested': False
        }

    def test_create_user(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(user.username, self.user_data['username'])
        self.assertEqual(user.email, self.user_data['email'])
        self.assertTrue(user.check_password(self.user_data['password']))
        self.assertEqual(user.role, CustomUser.CUSTOMER)
        self.assertFalse(user.is_owner_requested)
        self.assertTrue(user.created_at)
        self.assertTrue(user.updated_at)

    def test_create_user_without_email(self):
        user_data = self.user_data.copy()
        user_data['email'] = ''
        with self.assertRaises(ValidationError):
            CustomUser.objects.create_user(**user_data)

    def test_create_superuser(self):
        superuser = CustomUser.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword123'
        )
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)
        self.assertEqual(superuser.role, CustomUser.CUSTOMER)
        self.assertFalse(superuser.is_owner_requested)

    def test_unique_email(self):
        CustomUser.objects.create_user(**self.user_data)
        user_data_duplicate = self.user_data.copy()
        user_data_duplicate['username'] = 'testuser2'
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(**user_data_duplicate)

    def test_role_choices(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertIn(user.role, [CustomUser.CUSTOMER, CustomUser.OWNER])
        user.role = CustomUser.OWNER
        user.save()
        self.assertEqual(user.role, CustomUser.OWNER)

    def test_phone_number_optional(self):
        user_data_no_phone = self.user_data.copy()
        user_data_no_phone['phone_number'] = ''
        user = CustomUser.objects.create_user(**user_data_no_phone)
        self.assertEqual(user.phone_number, '')

    def test_profile_picture_upload(self):
        image_content = b'fake image content'
        image = SimpleUploadedFile('test.jpg', image_content, content_type='image/jpeg')
        user = CustomUser.objects.create_user(**self.user_data)
        user.profile_picture = image
        user.save()
        self.assertTrue(user.profile_picture)
        self.assertTrue(os.path.exists(user.profile_picture.path))
        user.profile_picture.delete()

    def test_is_owner_requested_default(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertFalse(user.is_owner_requested)
        user.is_owner_requested = True
        user.save()
        self.assertTrue(user.is_owner_requested)

    def test_groups_and_permissions(self):
        user = CustomUser.objects.create_user(**self.user_data)
        group = Group.objects.create(name='test_group')
        permission = Permission.objects.create(
            name='test_permission',
            content_type_id=1,
            codename='test_perm'
        )
        user.groups.add(group)
        user.user_permissions.add(permission)
        self.assertIn(group, user.groups.all())
        self.assertIn(permission, user.user_permissions.all())

    def test_str_method(self):
        user = CustomUser.objects.create_user(**self.user_data)
        self.assertEqual(str(user), self.user_data['username'])

    def test_updated_at_changes(self):
        user = CustomUser.objects.create_user(**self.user_data)
        initial_updated_at = user.updated_at
        user.phone_number = '+994987654321'
        user.save()
        self.assertNotEqual(user.updated_at, initial_updated_at)
