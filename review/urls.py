from django.urls import path
from .import views


urlpatterns=[
    path("restaurants/<int:restaurant_id>/reviews/",views.ReviewListView.as_view(),name="review-list"),
    path("reviews/<int:review_id>/",views.ReviewDetailView.as_view(),name="review-detail"),
]