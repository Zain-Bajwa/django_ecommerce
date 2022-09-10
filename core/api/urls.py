"""Product APIs URL Configuration

This file contains all the URLs of the core APIs Application. This file is
used to connect the URLs to the views. In this file we have used the JWT
Token authentication to access the views.
"""

from django.urls import path
from rest_framework import routers
from .views import (
    AddToCartView,
    AllProductViewSet,
    AllCategoryViewSet,
    CartView,
    CategoryViewSet,
    CategoryProductView,
    ProductViewSet,
    CreateReviewView,
    RemoveFromCartView,
    OrderPlaceView,
    OrderDetailView,
    RatingListViewSet,

)

# pylint: disable=invalid-name
app_name = 'api'
router = routers.DefaultRouter()

# For retrieve, update, and delete a Category
router.register("category", CategoryViewSet, basename="category-view")
# For retrieve all the categories
router.register("categories", AllCategoryViewSet, basename="categories-view")

# For retrieve a Product
router.register('product', ProductViewSet, basename='product-view')
# For retrieve all the products
router.register("products", AllProductViewSet, basename="products-view")

# Display all Reviews
router.register('review', RatingListViewSet, basename='rating-view')

urlpatterns = [
    path(
        "products/<str:gategory_name>/",
        CategoryProductView.as_view(),
        name="category-products-view",
    ),
    path("cart/add/", AddToCartView.as_view(), name="add-to-cart"),
    path("cart/view/<int:user_id>/", CartView.as_view(), name="cart-view"),
    path("cart/remove", RemoveFromCartView.as_view(), name="remove-from-cart"),
    path("order/place", OrderPlaceView.as_view(), name="place-order-view"),
    path("order/detail", OrderDetailView.as_view(), name="order-detail-view"),
    path(
        "product/review/create/<int:user_id>",
        CreateReviewView.as_view(),
        name='create-review'
    ),

]

urlpatterns += router.urls
