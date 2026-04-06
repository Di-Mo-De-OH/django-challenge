from rest_framework import status
from rest_framework.test import APITestCase

from restaurant.models import RestaurantModel
from user.models import UserModel
from review.models import ReviewModel
from django.urls import reverse


class ReviewAPIViewTestCase(APITestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            nickname = "test",
            email = "test@test.com",
            password = "testpassword1",
        )
        self.restaurant = RestaurantModel.objects.create(
            name= "restaurant",
        address= "address",
        contact= "contact",
        open_time= "10:00:00",
        close_time = "18:40:00",
        last_order = "18:00:00",
        regular_holiday ="MON",
        )
        self.data = {
            "restaurant": self.restaurant,
            "user": self.user,
            "title":"title",
            "comment":"comment",
        }
        self.client.login(email='test@test.com', password='testpassword1')

    def test_get_review_list(self):
        self.review = ReviewModel.objects.create(
            **self.data
        )
        url = reverse("review-list",kwargs={"restaurant_id":self.restaurant.id})

        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data.get("results")),1)
        self.assertEqual(response.data.get("results")[0].get("title"), self.review.title)
        self.assertEqual(response.data.get("results")[0].get("comment"), self.review.comment)
        self.assertEqual(response.data.get("results")[0].get("user")["id"], self.user.id)
        self.assertEqual(response.data.get("results")[0].get("restaurant")["id"], self.restaurant.id)



    def test_post_review(self):
        url = reverse("review-list",kwargs={"restaurant_id":self.restaurant.id})
        post_data = {**self.data, "restaurant": self.restaurant.id, "user": self.user.id}
        response = self.client.post(
                url,
                post_data
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("title"),self.data["title"])
        self.assertEqual(response.data.get("comment"), self.data["comment"])
        self.assertEqual(response.data.get("user")["id"],self.user.id)
        self.assertEqual(response.data.get("restaurant")["id"], self.restaurant.id)

    def test_get_review_detail(self):
        self.review = ReviewModel.objects.create(**self.data)
        url =reverse("review-detail",kwargs={"review_id":self.review.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("title"),self.data["title"])
        self.assertEqual(response.data.get("comment"), self.data["comment"])
        self.assertEqual(response.data.get("user")["id"], self.user.id)
        self.assertEqual(response.data.get("restaurant")["id"], self.restaurant.id)

    def test_update_review(self):
        self.review = ReviewModel.objects.create(**self.data)
        url = reverse("review-detail", kwargs={"review_id": self.review.id})
        data = {
            "title":"updated title",
            "comment":"updated comment",
        }
        response = self.client.put(url,data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.get("title"), data["title"])
        self.assertEqual(response.data.get("comment"), data["comment"])

    def test_delete_review(self):
        self.review = ReviewModel.objects.create(**self.data)
        url = reverse("review-detail", kwargs={"review_id": self.review.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)
        self.assertFalse(ReviewModel.objects.filter(id=self.review.id).exists())
        self.assertEqual(ReviewModel.objects.count(), 0)

