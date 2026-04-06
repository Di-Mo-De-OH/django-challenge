from rest_framework import serializers
from .models import RestaurantModel

# name = models.CharField(max_length=50)
#     address = models.CharField(max_length=200)
#     contact = models.CharField(max_length=50)
#     open_time = models.TimeField(null=True,blank=True)
#     close_time = models.TimeField(null=True,blank=True)
#     last_order = models.TimeField(null=True,blank=True)
#     regular_holiday = models.CharField(max_length=3,choices = DAYS_OF_WEEK,null = True,blank=True)




class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = RestaurantModel
        fields = [
            "id",
            "name",
            "address",
            "contact",
            "open_time",
            "close_time",
            "last_order",
            "regular_holiday",
        ]
