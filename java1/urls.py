"""
URL configuration for java1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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



from django.contrib import admin
from django.urls import path

from product.views import HomePage, MyLoginView, logout_view, search, category_page, product_page, \
    add_product_to_user_cart, user_cart, delete_user_cart
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',HomePage.as_view(), name='home'),
    path('login/', MyLoginView.as_view()),
    path('logout/', logout_view),
    path('search', search),
    path('products/<int:pk>', product_page),
    path('category/<int:pk>', category_page),
    path('add_to_cart/<int:pk>', add_product_to_user_cart),
    path('user_cart', user_cart),
    path('delete_cart/<int:pk>',delete_user_cart)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
