# Ecommerce API
### Documentation:

1. [Django](https://docs.djangoproject.com/en/4.0/)
2. [Django Rest Framework](https://www.django-rest-framework.org/)


### Installation

- In your required directory clone the repository `django_ecommerce` with the following command:

    `git clone https://github.com/Zain-Bajwa/django_ecommerce.git`

- Go to the directory `django_ecommerce`

    `cd django_ecommerce`

- In your current directory create a [virtual environment](https://docs.python.org/3/library/venv.html#creating-virtual-environments) by running the following command:

    `python3 -m venv .venv`

    ".venv" is the name of your virtual environment. You can also run with `python`.
- Run the following command to activate the virtual environment:

    `source .venv/bin/activate`

- Install all libraries of [requirements.txt]()

    `python3 -m pip install -r requirements.txt`

### Django Setup
- Create `Django` project

    `django-admin startproject ecommerece`
- Go to the directory `ecommerence` and create an App `authentication`

    `django-admin startapp user_api`

- Install using `Django Rest Framework`

    `pip install djangorestframework`

Add `'rest_framework'` to your `INSTALLED_APPS` in setting.py.
```pyhton
INSTALLED_APPS = [
    ...
    'rest_framework',
]
```
- Run [manage.py]() directly.

    `python3 manage.py runserver`
