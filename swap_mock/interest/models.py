from django.db import models
from .choices import (
    ASSET_TYPES, CONSORTIUMS,
    WEIGHTS, TRANSACTION_TYPES,
    BENCHMARKS
)
from django.db.models.signals import pre_save
from .constants import SECRET_PASSPHRASE, PUBLIC_ADDRESS, PUBLIC_KEY
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core import serializers
import json
import hashlib
from binascii import hexlify

# Create your models here.


class Asset(models.Model):
    # Interest Rate Forms Fields
    assetType = models.CharField(choices=ASSET_TYPES, max_length=100)
    description = models.TextField()
    interestRate = models.DecimalField(decimal_places=10, max_digits=20)
    floating = models.BooleanField()
    basis = models.CharField(choices=BENCHMARKS, max_length=100, blank=True)

    # SWAPBlocks Requirements
    amount = models.BigIntegerField()
    consortium = models.CharField(choices=CONSORTIUMS,
                                  blank=True, max_length=255)
    registrar = models.CharField(max_length=255, blank=True) # Users public address
    weight = models.IntegerField(choices=WEIGHTS, default=0)
    validThrough = models.DateTimeField()
    UAI = models.CharField(max_length=255, blank=True) # Unique asset ID
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"AssetId: {self.UAI}"


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
    confirmations = models.IntegerField(default=0, blank=True)
    transactionId = models.CharField(max_length=255, blank=True)
    consortiumPacket = models.TextField(blank=True)
    municipalPacket = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction: {self.transactionId}"

    class Meta:
        ordering = ['-timestamp']


class OrderBook(models.Model):
    mempool = models.ManyToManyField(Transaction, blank=True)


@receiver(post_save, sender=Asset)
def asset_post_save(sender, instance, created=False, **kwargs):
    """ UAI and registrar setting """
    if created:
        try:
            # Set registrar to users public address
            instance.registrar = PUBLIC_ADDRESS
            instance.save()

            # serialize object and extract fields needed for hashing
            serial_asset = serializers.serialize('json', [instance, ])
            json_asset = json.loads(serial_asset)
            needed_fields = json_asset[0]['fields']
            consortiumpacket_keys = ['assetType', 'basis',
                       'description', 'floating']
            oth_keys = ['amount', 'consortium',
                        'registrar', 'weight', 'validThrough']

            # create 2 dicts 1 of data_packet1 and one for standard data
            # Convert each dict into encoded json
            consortium_packet  = json.dumps({key: needed_fields[key]
                                   for key in consortiumpacket_keys}).encode()
            standard_data = json.dumps({key: needed_fields[key]
                             for key in oth_keys}).encode()

            # hash each byte string sha3_256
            packet_hash = hashlib.sha3_256(consortium_packet).digest()
            standard_data = hashlib.sha3_256(standard_data).digest()
            # Concatenate byte strings dp1 + stnd, hash it and convert to hex
            uai_bytes = hashlib.sha3_256(packet_hash + standard_data).digest()
            UAI = f"{instance.weight}{hexlify(uai_bytes).decode()}"

            # Set and save
            instance.UAI = UAI
            instance.save()

            # Now create a new asset genesis transaction
            Transaction.objects.create(
                amount=instance.amount,
                transactionType="assetGenesis",
                standardAsset=instance,
                receipeint=PUBLIC_ADDRESS,
                consortiumPacket=consortium_packet
            )
            # Broadcast transaction to the network
            print(f"""
                  Transaction is being broadcast to the network
                  for asset {UAI}
                  """)
        except Exception as e:
           # Do other stuff
            print(e)


@receiver(post_save, sender=Transaction)
def transaction_post_save(sender, instance, created=False, **kwargs):
    """ Set the sender. """
    if created:
        try:
            # Set sender to the senders public address
            instance.sender = PUBLIC_ADDRESS
            instance.save()

            serial_asset = serializers.serialize('json', [instance, ])
            json_asset = json.loads(serial_asset)
            needed_fields = json_asset[0]['fields']
            keys = ['transactionType', 'sender', 'receipeint', 'amount']
            tType = instance.transactionType
            if tType != "currency":
                if tType != 'assetSwap':
                    keys.append('standardAsset')
                    needed_fields['standardAsset'
                                  ] = instance.standardAsset.UAI
                if tType == 'assetSwap':
                    keys.append('makerAsset')
                    keys.append('takerAsset')
                    needed_fields['makerAsset'
                                  ] = instance.makerAsset.UAI
                    needed_fields['takerAsset'
                                  ] = instance.takerAsset.UAI

                # Add transaction sections to hash based on transaction type
                # pass
            standard_data = json.dumps({key: needed_fields[key]
                for key in keys}).encode()
            # Concatenate byte strings dp1 + stnd, hash it and convert to hex
            id_bytes = hashlib.sha3_256(packet_hash + standard_data).digest()
            transactionID = hexlify(id_bytes)
            instance.transactionId = transactionID.decode()

            # Set and save
            instance.save()

        except Exception as e:
            # Do nothing
            print(e)
