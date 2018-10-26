from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from .models import Transaction, Asset
from .forms import IndexAssetForm, TransactionForm
from django.contrib import messages
from django.core import serializers
import json
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from pprint import pprint
# Create your views here.


class AssetListView(ListView):

    model = Asset
    paginage_by = 2


class AssetDetailView(DetailView):

    model = Asset


def home(request):
    """
    Renders the first page  which should display a default ETF(index) asset
    with live value data from coinmarketcap.com
    """
    context = {"asset1": "UAI04ff9a3da154fcba054aa7ff4b1ad43def3e057cd23131753de97d69175f5bbcf",
               "asset2": "UAI1b70310e013c00bed2ba22b5fe423c1bfb8b94f148d2a52031b944ae6fd002208"}
    return render(request, "interest/index.html", context)

def order_book(request):
    """
    Order book view should allow order transactions to be placed and should
    show all open orders
    """
    return render(request, "interest/orderbook.html", {})

def create_asset(request):
    """ Creates and asset genesis transaction"""
    index_asset_form = IndexAssetForm(request.POST or None)
    context = {"IndexAssetForm": index_asset_form}
    if request.POST:
        if index_asset_form.is_valid():
            index_asset_form.save()
            index_asset_form = IndexAssetForm(request.POST or None)
            message = f"Raw Asset: {last_asset()}"
            messages.success(request, f"Success Asset Created {message}")
    return render(request, "interest/asset.html", context)

def create_transaction(request):
    """
    Allows for users to create transactions from scratch using assets
    in their wallet
    """
    transaction_form = TransactionForm(request.POST or None)
    context = {"TransactionForm": transaction_form}
    if request.POST:
        if transaction_form.is_valid():
            transaction_form.save()
            transaction_form = TransactionForm(request.POST or None)
            message = f"Raw Transaction: {last_transaction()}"
            messages.success(request,
                             f"Success Transaction Created: {message}")
    return render(request, "interest/transaction.html", context)


def index_lookup(UAI):
    transactions = Transaction.objects.filter(standardAsset__UAI=UAI)
    last_t = transactions.last()
    try:
        data = json.loads(last_t)
    except:
        print('NOT VALID JSON')
        data = {"error": "no_data"}
    return data


def last_asset():
    """
    Return latest asset as json.
    """
    last_asset = Asset.objects.latest('timestamp')
    serial_asset = serializers.serialize('json', [last_asset])
    json_asset = json.loads(serial_asset)
    needed_fields = json_asset[0]['fields']
    needed_fields.pop('timestamp')
    transaction = last_transaction()
    needed_fields['transactionId'] = transaction['transactionId']
    return needed_fields


def last_transaction():
    """
    Return latest transaction as json
    """
    last_transaction = Transaction.objects.latest('timestamp')
    serial_transaction = serializers.serialize('json', [last_transaction])
    json_transaction = json.loads(serial_transaction)
    needed_fields = json_transaction[0]['fields']
    needed_fields.pop('timestamp')
    pprint(needed_fields)
    return needed_fields


def get_latest_coin_prices(coin_list):
    API_KEY_CMC = "8655fbd5-ceac-4ac5-a891-5bc2a437acf7"
    headers = {'X-CMC_PRO_API_KEY': API_KEY_CMC}
    try:
        coins = ",".join(coin_list)
        uri = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coins}&convert=USD"
        latest_req = requests.get(uri, headers=headers)
        content = json.loads(latest_req.content.decode())
        prices = {}
        for coin in content['data']:
            prices[coin] = content['data'][coin]['quote']['USD']['price']
    except:
        print(content)
    return prices


# ETF
# Index fund create view where someone can add a new index fund

# Index fund update view where the consortium packet is updated with the new
# contents

# Index fund search view, where indexs can be looked up by using the UAI
# y = Transaction.objects.filter(standardAsset__UAI=asset_uai)
# x = y.last()
#k
