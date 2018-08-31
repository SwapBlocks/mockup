from django.db import models
from .choices import ASSET_TYPES, CONSORTIUMS, WEIGHTS, TRANSACTION_TYPES
# Create your models here.


class Asset(models.Model):
    # Interest Rate Forms Fields
    assetType = models.CharField(choices=ASSET_TYPES)
    description = models.TextField()
    interestRate = models.DecimalField()
    floating = models.BooleanField()
    amount = models.CharField()

    # SWAPBlocks Requirements
    consortium = models.CharField(choices=CONSORTIUMS, blank=True)
    registrar = models.CharField() # Users public key
    weight = models.IntegerField(choices=WEIGHTS, default=0)
    validThrough = models.DateTimeField(auto_now_add=True)
    UAI = models.CharField(max_length=255, blank=True) # Unique asset ID

    def __str__(self):
        return f"AssetId: {self.UAI}"

class Transaction(models.Model):
    transactionType = models.CharField(choices=TRANSACTION_TYPES)
    sender = models.CharField(max_length=255)
    receipeint = models.CharField(max_length=255)
    amount = models.IntegerField()
    asset = models.ForeignKey(Asset, blank=True)
    confirmations = models.IntegerField(blank=True)
    transactionId = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Transaction: {self.transactionId}"
