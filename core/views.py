"""Views of Core Django Templates

This module has all core views of ecommerce. These views are Django Template
Views. All views are used to render html pages. We used extedn model to exted
the template. We have a layout.html file. All other html files are extended
with layout.html.
"""

from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Count
from django.db.models.functions import Round
from authentication.models import User
from core.models import Product, Cart, Order, OrderItem


# pylint: disable=no-member
class HomeView(TemplateView):
    """HomeView

    This view is created for home page.
    """

    template_name = "core/home.html"
    model = Product

    def get_queryset(self):
        """Override the get_queryset() function for gettin desired data"""

        return Product.objects.annotate(
            count=Count("productreview__rating"),
            avg_rating=Round(Avg("productreview__rating")),
            no_rating=5 - Round(Avg("productreview__rating")),
        )


class AboutView(TemplateView):
    """AboutView

    This view is created for about page.
    """

    template_name = "core/about.html"


class ProfileView(TemplateView):
    """ProfileView

    This view is created for user profile page.
    """

    template_name = "core/Profile.html"


class OrderDetailView(ListView):
    """OrderDetailView

    This view is created for detail of the product page.
    """

    model = OrderItem
    template_name = "core/Order_detail.html"

    def get_context_data(self, **kwargs):
        """Override the get_context_data() function to add user informatio in
        the context"""

        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context

    def get_queryset(self):
        """Override the get_queryset() function for gettin desired data"""

        order_id = self.kwargs["pk"]
        return OrderItem.objects.filter(order__id=int(order_id))


class OrderListView(ListView):
    """OrderListView

    This view is created for list of all orders of a user page.
    """

    model = Order
    template_name = "core/Order_list.html"

    def get_context_data(self, **kwargs):
        """Override the get_context_data() function to add user informatio in
        the context"""
        context = super().get_context_data(**kwargs)
        context["user"] = User.objects.get(pk=self.kwargs["pk"])
        return context


class ContactView(TemplateView):
    """ContactView

    This view is created for contact page.
    """

    template_name = "core/contact.html"


class CartView(ListView):
    """CartView

    This view is created to display the product in the cart of a user.
    """

    model = Cart
    template_name = "core/Cart.html"

    def get_queryset(self):
        """Override the get_queryset() function for gettin desired data"""

        return Cart.objects.filter(user__id=self.kwargs["pk"])


class ProductDetailView(DetailView):
    """ProductDetailView

    This view is created to display detail of a product.
    """

    model = Product
    template_name = "core/Product_detail.html"


class ProductListView(ListView):
    """ProductListView

    This view is created to display all products.
    """

    template_name = "core/Product_list.html"
    model = Product

    def get_queryset(self):
        """Override the get_queryset() function for gettin desired data"""

        return Product.objects.annotate(
            count=Count("productreview__rating"),
            avg_rating=Round(Avg("productreview__rating")),
            no_rating=5 - Round(Avg("productreview__rating")),
        )
