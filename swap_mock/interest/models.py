from django.db import models
from .choices import (
    ASSET_TYPES, CONSORTIUMS,
    WEIGHTS, TRANSACTION_TYPES,
    BENCHMARKS
)
from datetime import datetime, timedelta


def default_end_time():
    now = datetime.now()
    return now + timedelta(days=365)

# Create your models here.


class Asset(models.Model):
    # SWAPBlocks Requirements
    amount = models.BigIntegerField()
    consortium = models.CharField(choices=CONSORTIUMS,
                                  blank=True, max_length=255)
    registrar = models.CharField(max_length=255, blank=True) # Users public address
    weight = models.IntegerField(choices=WEIGHTS, default=0)
    validThrough = models.DateTimeField(default=default_end_time)
    UAI = models.CharField(max_length=255, blank=True) # Unique asset ID
    consortiumPacket = models.TextField(blank=True)
    municipalPacket = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AssetId: {self.UAI}"

    class Meta:
        ordering = ['timestamp']


class Transaction(models.Model):
    transactionType = models.CharField(choices=TRANSACTION_TYPES,
                                       max_length=50)
    sender = models.CharField(max_length=255)
    receipeint = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=40, decimal_places=10)
    standardAsset = models.ForeignKey(Asset, on_delete=models.CASCADE,
                                          blank=True, null=True,
                                          related_name="asset")
    makerAsset = models.ForeignKey(Asset, on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name="makerAsset")
    takerAsset = models.ForeignKey(Asset, on_delete=models.CASCADE,
                                   blank=True, null=True,
                                   related_name="takerAsset")
    consortium = models.CharField(choices=CONSORTIUMS,
                                  blank=True, max_length=255)
    transactionId = models.CharField(max_length=255, blank=True)
    consortiumPacketHash = models.CharField(max_length=64, blank=True)
    municipalPacketHash = models.CharField(max_length=64, blank=True)
    consortiumPacket = models.TextField(blank=True)
    municipalPacket = models.TextField(blank=True)
    confirmations = models.IntegerField(default=0, blank=True)
    validThrough = models.DateTimeField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.transactionId}"

    class Meta:
        ordering = ['timestamp']


class OrderBook(models.Model):
    mempool = models.ManyToManyField(Transaction, blank=True)
