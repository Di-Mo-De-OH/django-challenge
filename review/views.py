from django.http import Http404
from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from restaurant.models import RestaurantModel
from review.models import ReviewModel
from review.serializers import ReviewSerializer,ReviewDetailSerializer


class ReviewListView(ListCreateAPIView):
    queryset = ReviewModel.objects.all().order_by('-created_at')
    serializer_class =ReviewSerializer
    def get_queryset(self):
        queryset = ReviewModel.objects.filter(restaurant_id=self.kwargs['restaurant_id'])
        return queryset

    def perform_create(self,serializer):
        restaurant_id = self.kwargs['restaurant_id']
        try:
            restaurant = RestaurantModel.objects.get(id=restaurant_id)
        except RestaurantModel.DoesNotExist:
            raise Http404
        serializer.save(restaurant=restaurant,user=self.request.user)

class ReviewDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        review_id = self.kwargs['review_id']
        try:
            review = ReviewModel.objects.get(id=review_id,user = self.request.user)
        except ReviewModel.DoesNotExist:
            raise Http404
        return review


