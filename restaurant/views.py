from .serializers import RestaurantSerializer
from rest_framework import viewsets
from .models import RestaurantModel

class RestaurantView(viewsets.ModelViewSet):
    queryset = RestaurantModel.objects.all()
    serializer_class = RestaurantSerializer

