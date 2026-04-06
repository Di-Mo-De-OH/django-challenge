from django.contrib.auth.hashers import check_password
from django.db.models import Model
from rest_framework.test import APITestCase
from user.models import UserModel
from django.urls import reverse

class UserAPIViewTest(APITestCase):
    def setUp(self):
        self.data = {
            "nickname":"test",
            "email":"test@test.com",
            "password":"testpassword1",
        }


    def test_user_signup(self):
        response = self.client.post(reverse('user-signup'), self.data)
        self.assertEqual(response.status_code,201)
        self.assertEqual(UserModel.objects.count(),1)
        self.assertEqual(response.data.get("nickname"),self.data["nickname"])
        self.assertEqual(response.data.get("email"),self.data["email"])



    def test_user_login(self):
        user = UserModel.objects.create_user(**self.data)
        data = {
            "nickname": "test",
            "email": "test@test.com",
            "password": "testpassword1",
        }
        response = self.client.post(reverse("user-login"),data)

        self.assertEqual(response.status_code,200)
        self.assertIn("message",response.data)
        self.assertEqual(response.data.get("message"),"login successful.")

    def test_get_login_invalid_credentials(self):
        data = {
            "nickname": "test",
            "email": "test@test.com",
            "password": "testpassword1",
        }
        response = self.client.post(reverse("user-login"),data)
        self.assertEqual(response.status_code,400)


    def test_user_details(self):
        user = UserModel.objects.create_user(**self.data)
        self.client.login(email=self.data["email"],password = self.data["password"])
        response = self.client.get(reverse("user-details",kwargs={"pk":user.pk}))
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data.get("nickname"),self.data["nickname"])
        self.assertEqual(response.data.get("email"),self.data["email"])




    def test_update_user(self):
        user = UserModel.objects.create_user(**self.data)
        self.client.login(
            email=self.data["email"],
            password=self.data["password"],
        )
        data = {
            "nickname": "testupdate",
            "email": "test-update@test.com",
            "password":"testpassword1",
        }
        response = self.client.patch(reverse("user-details",kwargs = {"pk":user.pk}),data=data)
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.data.get("nickname"),data["nickname"])
        user.refresh_from_db()
        self.assertTrue(check_password('testpassword1', user.password))


    def test_delete_user(self):
        user = UserModel.objects.create_user(**self.data)
        self.client.login(
            email=self.data["email"],
            password=self.data["password"],

        )
        response = self.client.delete(reverse("user-details",kwargs={"pk":user.pk}))

        self.assertEqual(response.status_code,204)
        self.assertFalse(UserModel.objects.filter(email='test@example.com').exists())



