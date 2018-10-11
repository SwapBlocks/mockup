from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    """
    Renders the first page  which should display a default ETF(index) asset
    with live value data from coinmarketcap.com
    """
    return render(request, "interest/index.html", {})

def order_book(request):
    """
    Order book view should allow order transactions to be placed and should
    show all open orders
    """
    return  HttpResponse("Order Book View")

def create_asset(request):
    """ Creates and asset genesis transaction"""
    return HttpResponse("Create New Asset View")

def create_transaction(request):
    " Allows for users to create transactions from scratch"
    return HttpResponse("Create transaction View")



# ETF
# Index fund create view where someone can add a new index fund

# Index fund update view where the consortium packet is updated with the new
# contents

# Index fund search view, where indexs can be looked up by using the UAI

