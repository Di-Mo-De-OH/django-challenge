from django.test import TestCase

from restaurant.models import RestaurantModel



class RestaurantModelTest(TestCase):
    def setUp(self):
        self.restaurant = {
            "name":"restaurant",
            "address":"address",
            "contact":"contact",
            "open_time":"10:00:00",
            "close_time":"18:40:00",
            "last_order":"18:00:00",
            "regular_holiday":"MON",
        }



    def test_create_restaurant(self):
        restaurant = RestaurantModel.objects.create(
            **self.restaurant
        )
        self.assertEqual(RestaurantModel.objects.count(),1)
        self.assertEqual(restaurant.name,self.restaurant["name"])
        self.assertEqual(restaurant.address, self.restaurant["address"])
        self.assertEqual(restaurant.contact, self.restaurant["contact"])
        self.assertEqual(restaurant.open_time, self.restaurant["open_time"])
        self.assertEqual(restaurant.close_time, self.restaurant["close_time"])
        self.assertEqual(restaurant.last_order, self.restaurant["last_order"])
        self.assertEqual(restaurant.regular_holiday, self.restaurant["regular_holiday"])

