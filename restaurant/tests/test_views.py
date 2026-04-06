from django.test import TestCase
from rest_framework import status

from restaurant.models import RestaurantModel
from user.models import UserModel
from django.urls import reverse


class RestaurantViewTests(TestCase):
    def setUp(self):
        self.restaurant = {
            "name": "restaurant",
            "address": "address",
            "contact": "contact",
            "open_time": "10:00:00",
            "close_time": "18:40:00",
            "last_order": "18:00:00",
            "regular_holiday": "MON",
        }
        self.user = UserModel.objects.create_user(
            nickname ="test",
            email = "test@test.com",
            password = "testpassword1",
        )
        self.client.login(email='test@test.com', password='testpassword1')

    def test_restaurant_list_view(self):
        url = reverse('restaurant-list')
        RestaurantModel.objects.create(**self.restaurant)
        response = self.client.get(url)
        response_data = response.data.get('results')[0].get
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(response.data.get("results")),1)
        self.assertEqual(response_data("name"),self.restaurant["name"])
        self.assertEqual(response_data("address"), self.restaurant["address"])
        self.assertEqual(response_data("contact"), self.restaurant["contact"])
        self.assertEqual(response_data("open_time"), self.restaurant["open_time"])
        self.assertEqual(response_data("close_time"), self.restaurant["close_time"])
        self.assertEqual(response_data("last_order"), self.restaurant["last_order"])
        self.assertEqual(response_data("regular_holiday"), self.restaurant["regular_holiday"])

    def test_restaurant_post_view(self):
        url = reverse("restaurant-list")
        response = self.client.post(url,self.restaurant,content_type="application/json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(RestaurantModel.objects.count(),1)
        self.assertEqual(RestaurantModel.objects.first().name,self.restaurant["name"])


    def test_restaurant_detail_view(self):
        restaurant = RestaurantModel.objects.create(**self.restaurant)
        url = reverse("restaurant-detail",kwargs = {"pk":restaurant.pk})

        response = self.client.get(url)
        self.assertEqual(response.status_code ,200)
        self.assertEqual(response.data.get("name"),self.restaurant["name"])
    def test_restaurant_update_view(self):
        restaurant = RestaurantModel.objects.create(**self.restaurant)
        url = reverse("restaurant-detail",kwargs = {"pk":restaurant.pk})
        updated_restaurant = {
            "name": "updated_restaurant",
            "address": "updated_address",
            "contact": "updated_contact",
            "open_time": "11:00:00",
            "close_time": "19:40:00",
            "last_order": "20:00:00",
            "regular_holiday": "MON",
        }

        response = self.client.put(url,updated_restaurant,content_type="application/json")
        response_data = response.data
        self.assertEqual(response.status_code,200)
        self.assertEqual(RestaurantModel.objects.count(),1)
        self.assertEqual(response_data["name"],updated_restaurant["name"])
        self.assertEqual(response_data["address"], updated_restaurant["address"])
        self.assertEqual(response_data["contact"], updated_restaurant["contact"])
        self.assertEqual(response_data["open_time"], updated_restaurant["open_time"])
        self.assertEqual(response_data["close_time"], updated_restaurant["close_time"])
        self.assertEqual(response_data["last_order"], updated_restaurant["last_order"])
        self.assertEqual(response_data["regular_holiday"], updated_restaurant["regular_holiday"])

    def test_restaurant_delete_view(self):
        restaurant = RestaurantModel.objects.create(**self.restaurant)
        url = reverse('restaurant-detail', kwargs={'pk': restaurant.pk})

        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertEqual(RestaurantModel.objects.count(), 0)
