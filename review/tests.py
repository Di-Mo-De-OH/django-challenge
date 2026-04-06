from django.test import TestCase

from restaurant.models import RestaurantModel
from user.models import UserModel
from.models import ReviewModel
# Create your tests here.


#
# user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name ="review")
# restaurant = models.ForeignKey(RestaurantModel,on_delete=models.CASCADE,related_name="review")
# title = models.CharField(max_length=50)
# comment = models.TextField()




class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            nickname="test",
            email = "test@test.com",
            password = "testpassword1",

        )
        self.restaurant = RestaurantModel.objects.create(
            name='restaurant',
            address='address',
            contact='Phone: 010-0000-0000'
        )
        self.review = {
            "user":self.user,
            "restaurant":self.restaurant,
            "title":"title",
            "comment":"comment",
        }
    def test_create_review(self):
        review = ReviewModel.objects.create(
           **self.review
        )

        self.assertEqual(review.title,self.review["title"])
        self.assertEqual(review.comment,self.review["comment"])
        self.assertEqual(review.user,self.user)
        self.assertEqual(review.restaurant,self.restaurant)


