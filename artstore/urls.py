"""
URL configuration for artstore project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from artapp.views import index, search, user_login, register_customer, logout_view, cart, add_to_cart, remove_from_cart, \
    info, confirmed
from artstore import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('search/', search, name='search_picture'),
    path('login/', user_login),
    path('register/', register_customer),
    path('logout/', logout_view, name='logout'),
    path('cart/', cart, name='cart'),
    path('add/<int:picture_id>/', add_to_cart, name='add'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('deliveryinfo/', info, name='info'),
    path('confirmed/', confirmed, name='order_confirmed'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
