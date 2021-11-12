from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse


class CustomUserTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='jeffrey',
            email='jeffrey@example.com',
            password='testpass123'
        )
        self.assertEqual(user.username, 'jeffrey')
        self.assertEqual(user.email, 'jeffrey@example.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='testpass123'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class LoginPageTests(TestCase):
    def setUp(self):
        url = reverse('account_login')
        self.response = self.client.get(url)

    def test_login_page_status_code(self):
        self.assertEqual(self.response.status_code, 200)

    def test_homepage_template(self):
        self.assertTemplateUsed(self.response, 'account/login.html')
