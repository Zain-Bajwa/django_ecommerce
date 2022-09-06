""" All Views of the Authentication Application

This file contains all the views of the authentication Application. The views
are used to create, update, delete and list the users. This file also contains
a custom permission class that is used to check if the user is related to the
that Toekn.

"""

# pylint: disable=no-member,too-many-ancestors

from rest_framework import generics, permissions, status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenViewBase
from django.core.exceptions import ObjectDoesNotExist
from .serializers import (
    UserRegisterSerializer,
    UserViewSerializer,
    CreateTokneSerialzer,
    CategoryViewSerializer,
    CartSerializer,
    ProductViewSerializer,
    OrderDetailSerializer,
    CreateTokneSerialzer,
)
from .models import Category, Product, User, Cart, Order, OrderItem


class UserRegisterView(generics.GenericAPIView):
    """User Registration View

    This view is used to create a new user. The user is created using the
    GenericAPIView class. The serializer is used to validate the data. The user
    is created and the data is returned.
    """

    serializer_class = UserRegisterSerializer

    def post(self, request):
        """Create the user"""

        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user_data = serializer.data

        return Response(user_data, status=status.HTTP_201_CREATED)


class OwnProfilePermission(permissions.BasePermission):
    """Custom Permission Class for the UserViewSet class

    This class is used to check if the user is related to his token. This class
    is used in the UserViewSet class. This class is inherited from the
    BasePermission to connect to the has_permission method.
    """

    def has_permission(self, request, view):
        """Check if the user is related to the token"""

        try:
            user_id = view.kwargs["user_id"]
            return request.user == User.objects.get(pk=user_id)
        except KeyError:
            try:
                return request.user == User.objects.get(pk=view.kwargs["pk"])
            except ObjectDoesNotExist:
                return request.user == request.user.is_authenticated


class UserViewSet(
    viewsets.GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    """User ViewSet
    This viewset is used to retrieve, update and delete a user. In this class
    JWT authentication is used to authenticate the user. This class also uses
    the OwnProfilePermission class to check if the user is related to his
    token.
    """

    queryset = User.objects.all()

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = UserViewSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """Inactivate the user"""
        return Response(
            User.objects.filter(pk=kwargs["pk"]).update(is_active=False),
            status=status.HTTP_204_NO_CONTENT,
        )


class IsSuperUser(permissions.BasePermission):
    """Custom Permission Class for the AllUserViewSet Class

    This class is used to check if the user is a superuser. This class is used
    in the AllUserViewSet class.
    """

    def has_permission(self, request, view):
        """Check if the user is a superuser"""

        return request.user and request.user.is_superuser


class AllUserViewSet(viewsets.GenericViewSet, ListModelMixin):
    """All User ViewSet
    This viewset is used to retrieve all the users. This class uses the JWT
    authentcation to authenticate the user.
    """

    queryset = User.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = UserViewSerializer


class CategoryViewSet(
    viewsets.GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    """Category ViewSet

    This viewset is used to retrieve, update and delete a category. In this
    class JWT authentication is used to authenticate the user. Only superusers
    are allowed to perform these actions.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]
    queryset = Category.objects.all()
    serializer_class = CategoryViewSerializer
    lookup_field = "pk"

    def destroy(self, request, *args, **kwargs):
        """Delete a category if it is not related to any product"""

        try:
            return super().destroy(request, *args, **kwargs)

        except Exception as e:
            product = Product.objects.filter(category__id=kwargs["pk"])
            serializer = ProductViewSerializer(product, many=True)
            return Response(
                {
                    "message": "This category is refered to product",
                    "Product": serializer.data,
                },
                status=status.HTTP_200_OK,
            )


class AllCategoryViewSet(
    viewsets.GenericViewSet, ListModelMixin, CreateModelMixin
):
    """All Category ViewSet

    This viewset is used to retrieve all the categories and also used to create
    an new category. This class uses the JWT authentcation to authenticate the
    user. Only superusers are allowed to perform these actions.
    """

    queryset = Category.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = CategoryViewSerializer


class CreateProductView(generics.CreateAPIView):
    """Create Product View

    This viewset is used to create a new product. This class uses the JWT
    authentication to authenticate the user. Only superusers are allowed to
    perform these actions.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductViewSerializer


class ProductViewSet(
    viewsets.GenericViewSet,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
):
    """Product ViewSet

    This viewset is used to retrieve, update and delete a product. In this
    class JWT authentication is used to authenticate the user. Only superusers
    are allowed to perform these actions.
    """

    queryset = Product.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = ProductViewSerializer
    lookup_field = "pk"


class AllProductViewSet(
    viewsets.GenericViewSet, CreateModelMixin, ListModelMixin
):
    """All Product ViewSet

    This viewset is used to retrieve all the products with GET method. It is
    also used to create a new product with POST method.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]

    queryset = Product.objects.all()
    serializer_class = ProductViewSerializer


class CategoryProductView(generics.ListAPIView):
    """All Product ViewSet

    This viewset is used to retrieve all the products according to category.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSuperUser]
    serializer_class = ProductViewSerializer

    def get_queryset(self):
        """
        This view should return a list of all the purchases for
        the user as determined by the username portion of the URL.
        """
        gategory_name = self.kwargs["gategory_name"]
        return Product.objects.filter(category__name=gategory_name)


class AddToCartView(generics.ListAPIView):
    """Add To Cart View

    This view is used to add a product to the cart. The product is added using
    the GenericAPIView class. This method is also used to update the Cart The
    serializer is used to validate the data. The product is added and the data
    is returned.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    queryset = Product.objects.all()
    serializer_class = CartSerializer

    def post(self, request, *args, **kwargs):
        """Add a product to the cart"""

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        # If the quantity is not provided then the quantity is set to 1
        try:
            quantity = serializer._validated_data["quantity"]
        except KeyError:
            quantity = 1

        user = serializer._validated_data["user"]
        product = serializer._validated_data["product"]

        # Check if the stock is available for the product
        if product.stock < quantity:
            return Response(
                {"message": "Available stock is " + str(product.stock)},
                status=status.HTTP_200_OK,
            )

        # Check if the product is not in the cart then add it to the cart
        if not Cart.objects.filter(user=user, product=product):
            serializer._validated_data["price"] = product.price * quantity
            serializer.save()
            instence = Cart.objects.filter(user=user)
            serializer = self.serializer_class(instence, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        try:
            # If the product is in the cart then update the quantity and price
            cart = Cart.objects.filter(user=user, product=product)
            total_price = product.price * quantity
            cart.update(quantity=quantity, price=total_price)

            instence = Cart.objects.filter(user=user)
            serializer = self.serializer_class(instence, many=True)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {"message": "Something went wrong"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class CartView(generics.ListAPIView):
    """Cart ViewSet

    This viewset is used to retrieve a cart. In this class JWT authentication
    is used to authenticate the user. User can view only his own cart.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = CartSerializer

    def get_queryset(self):
        """
        This view should return a list of all the products those are in cart
        for the user as determined by the user_id portion of the URL.
        """

        user_id = self.kwargs["user_id"]
        return Cart.objects.filter(user__id=user_id)


class RemoveFromCartView(generics.ListAPIView):
    """Remove From Cart View

    This view is used to remove a product from the cart. The serializer is used
    to validate the data. The product is removed and the data is returned.
    """

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, OwnProfilePermission]
    serializer_class = CartSerializer

    def delete(self, request, *args, **kwargs):
        """Remove a product from the cart"""

        user_id = request.query_params.get("user_id")
        product_id = request.query_params.get("product_id")
        if not user_id:
            return Response(
                {
                    "message": [
                        "User id is required in Url",
                        "Product id is optional in Url",
                    ]
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if product_id:
            if not Product.objects.filter(pk=int(product_id)):
                return Response(
                    {"message": "Not a valid Product"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if not User.objects.filter(pk=int(user_id)):
                return Response(
                    {"message": "Not a valid User"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if (
                Cart.objects.filter(
                    user__id=int(user_id), product__id=int(product_id)
                ).delete()[0]
                > 0
            ):
                return Response(
                    {"message": "Product removed from cart"},
                    status=status.HTTP_200_OK,
                )
            return Response(
                {"message": "Product is not in Cart"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if Cart.objects.filter(user__id=int(user_id)).delete()[0] > 0:
            return Response(
                {"message": "Cart cleared"}, status=status.HTTP_200_OK
            )

        return Response(
            {"message": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
        )


class OrderPlaceView(generics.GenericAPIView):
    """Place Order View

    This view is used to place an order. The order is placed using the
    GenericAPIView class. The serializer is used to validate the data. The
    order is placed and the success message is returned.
    """

    def post(self, request):
        """Place an order"""

        user_id = request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"message": "User id is required in query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.filter(pk=int(user_id))
            if user.count() > 0:
                cart = Cart.objects.filter(user=user[0])
                if cart.count() > 0:
                    order = Order.objects.create(user=user[0])
                    total_price = 0
                    for item in cart:
                        product = Product.objects.filter(pk=item.product.id)[0]
                        if product.stock < item.quantity:
                            return Response(
                                {
                                    "message": "Not enough stock for "
                                    + product.name
                                },
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    for item in cart:
                        OrderItem.objects.create(
                            order=order,
                            product=item.product,
                            quantity=item.quantity,
                            price=item.price,
                        )
                        Product.objects.filter(pk=item.product.id).update(
                            stock=product.stock - item.quantity
                        )
                        total_price += item.price
                        item.delete()
                    order.price = total_price
                    order.save()
                    return Response(
                        {"message": "Order placed"}, status=status.HTTP_200_OK
                    )
                else:
                    return Response(
                        {"message": "Cart is empty"}, status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    {"message": "Not a valid User"}, status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {"message": "Something went wrong"}, status=status.HTTP_200_OK
            )


class OrderDetailView(generics.ListAPIView):
    """Order Detail View

    This view is used to retrieve the order details. The order details are
    retrieved using the GenericAPIView class. The serializer is used to
    validate the data. The order details are retrieved and the data is
    returned.
    """

    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        """
        This view should return a list of all the orders those are placed for
        the user as determined by the user_id portion of the URL.
        """
        user_id = self.request.query_params.get("user_id")
        if not user_id:
            return Response(
                {"message": "User id is required in query parameter"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return OrderItem.objects.filter(order__user__id=int(user_id))


class CreateTokenView(TokenViewBase):
    """Create Token View

    This view is used to create a new token. This is inherited from the
    TokenViewBase of the rest_framework_simplejwt.views. The purpose of this
    view is to create a new token and override the default_error_message.
    """

    serializer_class = CreateTokneSerialzer