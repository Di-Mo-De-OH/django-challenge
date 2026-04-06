from django.test import TestCase
from user.models import UserModel
# Create your tests here.

class UserModelTest(TestCase):
    def setUp(self):
        self.test_user = {
            "email":"test@test.com",
            "nickname":"test",
            "password":"testpassword1"
        }
        self.test_admin_user = {
            'email': 'admin@test.com',
            'nickname': 'admintest',
            'password': 'adminpassword1',
            "is_superuser": True,
        }

    def test_user_manager_create_user(self):
        user = UserModel.objects.create_user(
            **self.test_user,
        )
        self.assertEqual(UserModel.objects.count(),1)
        self.assertEqual(user.email,"test@test.com")
        self.assertEqual(user.nickname,"test")
        self.assertTrue(user.check_password("testpassword1"))
        self.assertEqual(user.profile_image.url, '/media/users/blank_profile_image.png')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    def test_user_manager_create_superuser(self):
        user = UserModel.objects.create_superuser(
            **self.test_admin_user
        )
        self.assertEqual(UserModel.objects.filter(is_staff=True,is_superuser=True).count(),1)
        self.assertEqual(user.email,"admin@test.com")
        self.assertEqual(user.nickname,"admintest")
        self.assertTrue(user.check_password("adminpassword1"))
        self.assertTrue(user.is_active)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.profile_image.url, '/media/users/blank_profile_image.png')

