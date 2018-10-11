from django import forms
from .models import Asset, Transaction, OrderBook


class IndexAssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        field = ["amount", "consortium", "weight",
                 "validThrough", "consortiumPacket",]
        labels = {
            "amount": "Amount",
            "consortium": "Consortium",
            "weight": "Permission Level",
            "validThrough": "Valid To Date",
            "consortiumPacket": "Consortium Packet"
        }


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
