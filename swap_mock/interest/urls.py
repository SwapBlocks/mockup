"""interest url app
"""
from django.urls import path
from . import views


app_name = "interest"

urlpatterns = [
    path('', views.home, name="home"),
    path('orderbook', views.order_book, name="orderbook"),
    path('asset', views.create_asset, name="asset"),
    path('transaction', views.create_transaction, name="transaction"),
]
