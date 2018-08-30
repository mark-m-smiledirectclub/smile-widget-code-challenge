from django.contrib import admin
from django.urls import path

from rest_framework import routers

from products import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'api/get_price/', views.GetPriceView.as_view(), name='GetPriceView')
]

