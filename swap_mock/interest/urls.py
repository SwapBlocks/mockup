"""interest url app
"""
from django.urls import path
from . import views


app_name = "interest"

urlpatterns = [
    path('', views.home),
    path('orderbook', views.order_book),
    path('asset', views.create_asset),
    path('transaction', views.create_transaction),
]
