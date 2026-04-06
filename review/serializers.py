from rest_framework import serializers

from review.models import ReviewModel
from user.serializers import UserDetailSerializer
from restaurant.serializers import RestaurantSerializer

class ReviewSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)
    class Meta:
        model = ReviewModel
        fields = ["user","id","restaurant","title","comment"]
        read_only_fields = ["id","restaurant"]


class ReviewDetailSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    restaurant = RestaurantSerializer(read_only=True)

    class Meta:
        model = ReviewModel
        fields = ["user","id","restaurant","title","comment"]