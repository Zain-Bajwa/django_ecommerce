"""Authentication Application URL Configuration

This file contains all the URLs of the authentication Application. This file is
used to connect the URLs to the views. The URLs are used to create, update,
delete a user. It is also used to create new tokens, refresh and verify the
tokens. In this file we have used the rest_framework_simplejwt.views built-in
views to create, refresh and verify the tokens.
"""

from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)
from .views import (
    AddToCartView,
    AllProductViewSet,
    AllUserViewSet,
    CreateTokenView,
    AllCategoryViewSet,
    CartView,
    CategoryProductView,
    CategoryViewSet,
    ProductViewSet,
    CreateReviewView,
    RemoveFromCartView,
    UserRegisterView,
    UserViewSet,
    OrderPlaceView,
    OrderDetailView,
    LoginView,
    RegisterView,
    RatingListViewSet,

)

# pylint: disable=invalid-name
app_name = 'authentication'
router = routers.DefaultRouter()

# For retrieve, update, and delete a user
router.register("user", UserViewSet, basename="user-view")
# For retrieve all the users
router.register("users", AllUserViewSet, basename="users-view")

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
    path("register/user/", UserRegisterView.as_view(), name="register-user"),
    path("token/create/", CreateTokenView.as_view(), name="create-token"),
    path("token/refresh/", TokenRefreshView.as_view(), name="refresh-token"),
    path("token/verify/", TokenVerifyView.as_view(), name="verify-token"),
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
    path("login/", LoginView.as_view(), name="login-view"),
    path('register/', RegisterView.as_view(), name='register-view'),
]

urlpatterns += router.urls
