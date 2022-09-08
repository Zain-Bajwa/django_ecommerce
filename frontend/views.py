from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.
class HomeView(TemplateView):
    template_name = "home.html"


class LoginView(TemplateView):
    template_name = "login.html"


class RegisterView(TemplateView):
    template_name = "register.html"


class AboutView(TemplateView):
    template_name = "about.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class ProductView(TemplateView):
    template_name = "products.html"
