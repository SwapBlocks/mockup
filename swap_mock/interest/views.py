from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def home(request):
    return render(request, "interest/index.html", {})

def order_book(request):
    return  HttpResponse("Order Book View")

def create_asset(request):
    return HttpResponse("Create New Asset View")

def create_transaction(request):
    return HttpResponse("Create transaction View")
