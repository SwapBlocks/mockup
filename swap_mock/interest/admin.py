from django.contrib import admin
from .models import Asset, Transaction, OrderBook, InterestRateSwap
# Register your models here.

# admin.site.register(Asset)
admin.site.register(Transaction)
admin.site.register(OrderBook)
admin.site.register(InterestRateSwap)
