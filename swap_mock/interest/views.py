from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from .models import Transaction, Asset
from .forms import IndexAssetForm, TransactionForm
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
    return render(request, "interest/orderbook.html", {})

def create_asset(request):
    """ Creates and asset genesis transaction"""
    return render(request, "interest/asset.html", {})

def create_transaction(request):
    """
    Allows for users to create transactions from scratch using assets
    in their wallet
    """
    return render(request, "interest/transaction.html", {})

def index_lookup(UAI):
    transactions = Transaction.objects.filter(standardAsset__UAI=UAI)
    last_t = transactions.last()
    try:
        data = json.loads(last_t)
    except:
        print('NOT VALID JSON')
        data = {"error": "no_data"}
    return data


def get_coin_data(string_a_coin_name,string_start_date,string_end_date):
    coin_name = string_a_coin_name
    start_date = string_start_date
    end_date = string_end_date
    url = 'https://coinmarketcap.com/currencies/' + coin_name + '/historical-data/?start=' + start_date + '&end=' + end_date
    html = requests.get(url).content
    df_list = pd.read_html(html)
    df = df_list[-1]
    list_of_coin_data= df.values.tolist()
    return list_of_coin_data



# ETF
# Index fund create view where someone can add a new index fund

# Index fund update view where the consortium packet is updated with the new
# contents

# Index fund search view, where indexs can be looked up by using the UAI
# y = Transaction.objects.filter(standardAsset__UAI=asset_uai)
# x = y.last()
#k
