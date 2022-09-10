from django.views.generic.base import TemplateView
from django.views.generic import ListView, DetailView
from django.db.models import Avg, Count
from django.db.models.functions import Round
from .models import Product, Cart


# Create your views here.
class HomeView(ListView):
    template_name = "core/home.html"
    model = Product

    def get_queryset(self):

        queryset = Product.objects.annotate(
                count=Count('productreview__rating'),
                avg_rating=Round(Avg('productreview__rating')),
                no_rating= 5 - Round(Avg('productreview__rating'))
            )
        return queryset


class AboutView(TemplateView):
    template_name = "core/about.html"


class ContactView(TemplateView):
    template_name = "core/contact.html"

class CartView(ListView):
    # model = Cart
    template_name = "core/Cart.html"

    def get_queryset(self):

        queryset = Cart.objects.filter(user__id=self.kwargs['pk'])
        return queryset

class ProductDetailView(DetailView):
    model = Product
    template_name = "core/Product_detail.html"

class ProductListView(ListView):
    template_name = "core/Product_list.html"
    # login_url = ACCOUNT_LOGOUT_REDIRECT_URL
    # temp = loader.get_template('product_list.html')
    model = Product

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     products = Product.objects.all()
    #     for product in products:
    #         context["product"] = product
    #         context["rating"] = product.average_rating(product)
    #     # review = ProductReview.objects.filter(product__in=products)
    #     # context['input'] = q
    #     return context

    def get_queryset(self):

        queryset = Product.objects.annotate(
                count=Count('productreview__rating'),
                avg_rating=Round(Avg('productreview__rating')),
                no_rating= 5 - Round(Avg('productreview__rating'))
            )
        return queryset
