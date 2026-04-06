from django.db import models
from utils.basemodel import BaseModel
from user.models import UserModel
from restaurant.models import RestaurantModel

# Create your models here.
class ReviewModel(BaseModel):
    user = models.ForeignKey(UserModel,on_delete=models.CASCADE,related_name ="review")
    restaurant = models.ForeignKey(RestaurantModel,on_delete=models.CASCADE,related_name="review")
    title = models.CharField(max_length=50)
    comment = models.TextField()

