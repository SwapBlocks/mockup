from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Asset, Transaction
from .constants import SECRET_PASSPHRASE, PUBLIC_ADDRESS, PUBLIC_KEY
from django.core import serializers
import json
import hashlib
from binascii import hexlify
import codecs

@receiver(post_save, sender=Asset)
def asset_post_save(sender, instance, created=False, **kwargs):
    """
    UAI and registrar setting

    May need to update to add consortium and municipalPacket to transaction
    based on weight
    """
    if created:
        try:
            # Set registrar to users public address
            instance.registrar = PUBLIC_ADDRESS
            instance.save()

            # serialize object and extract fields needed for hashing
            serial_asset = serializers.serialize('json', [instance, ])
            json_asset = json.loads(serial_asset)
            needed_fields = json_asset[0]['fields']
            oth_keys = ['amount', 'consortium',
                        'registrar', 'weight', 'validThrough']

            # create 2 dicts 1 of data_packet1 and one for standard data
            # Convert each dict into encoded json
            consortium_data = needed_fields['consortiumPacket']

            municipal_data = needed_fields['municipalPacket']
            standard_data = json.dumps({key: needed_fields[key]
                             for key in oth_keys}, sort_keys=True).encode()

            # hash each byte string sha3_256
            if municipal_data:
                encoded_municipal_data = municipal_data.encode()
                municipal_packet_hash = hashlib.sha3_256(encoded_municipal_data
                                                      ).digest()
            else:
                municipal_packet_hash = b''
            if consortium_data:
                encoded_consortium_data = consortium_data.encode()
                consortium_packet_hash = hashlib.sha3_256(
                    encoded_consortium_data).digest()
            else:
                consortium_packet_hash = b''
            packet_to_hash = municipal_packet_hash + consortium_packet_hash
            if packet_to_hash:
                packet_hash = hashlib.sha3_256(packet_to_hash).digest()
            else:
                packet_hash = b''
            standard_data = hashlib.sha3_256(standard_data).digest()

            # Concatenate byte strings dp1 + stnd, hash it and convert to hex
            uai_bytes = hashlib.sha3_256(packet_hash + standard_data).digest()
            UAI = f"UAI{instance.weight}{hexlify(uai_bytes).decode()}"

            # Set and save
            instance.UAI = UAI
            instance.save()

            # Now create a new asset genesis transaction
            Transaction.objects.create(
                amount=instance.amount,
                transactionType="assetGenesis",
                standardAsset=instance,
                receipeint=PUBLIC_ADDRESS,
                consortiumPacket=consortium_data,
                consortiumPacketHash=consortium_packet_hash.hex(),
                municipalPacket=municipal_data,
                municipalPacketHash=municipal_packet_hash.hex()
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
                for key in keys}, sort_keys=True).encode()

            packet_hash = instance.municipalPacketHash.encode() + instance.consortiumPacketHash.encode()
            # Concatenate byte strings dp1 + stnd, hash it and convert to hex
            id_bytes = hashlib.sha3_256(packet_hash + standard_data
                                        ).digest()
            transactionID = hexlify(id_bytes)
            instance.transactionId = transactionID.decode()

            # Set and save
            instance.save()

        except Exception as e:
            # Do nothing
            print(e)

