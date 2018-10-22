from django import forms
from .models import Asset, Transaction, OrderBook


class IndexAssetForm(forms.ModelForm):

    class Meta:
        model = Asset
        fields = ["amount", "consortium", "weight",
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
        fields = ["transactionType", "receipeint", "amount",
                  "standardAsset", "makerAsset", "takerAsset",
                  "consortium", "consortiumPacket", "municipalPacket",
                  "validThrough"]
        labels = {"transactionType": "Transaction Type",
                  "receipeint": "Receipeint", "amount": "Amount",
                  "standardAsset": "Standard Asset",
                  "makerAsset": "Maker Asset", "takerAsset": "Taker Asset",
                  "consortium": "Consortium",
                  "consortiumPacket": "Consortium Packet",
                  "municipalPacket": "Municipal Packet",
                  "validThrough": "Valid Through"}
