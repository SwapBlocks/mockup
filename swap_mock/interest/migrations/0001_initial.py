# Generated by Django 2.1 on 2018-09-05 03:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Asset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assetType', models.CharField(choices=[('interestRateSwap', 'Interest Rate Swap'), ('realEstate', 'Real Estate'), ('creditDefaultSwap', 'Credit Default Swap'), ('futures', 'Futures Contract')], max_length=100)),
                ('description', models.TextField()),
                ('interestRate', models.DecimalField(decimal_places=10, max_digits=20)),
                ('floating', models.BooleanField()),
                ('basis', models.CharField(blank=True, choices=[('LIBOR', 'LIBOR'), ('TBILL', 'T-bill')], max_length=100)),
                ('amount', models.BigIntegerField()),
                ('consortium', models.CharField(blank=True, choices=[('someConsortiumHashId', 'Global Interest Rate Swap Group')], max_length=255)),
                ('registrar', models.CharField(max_length=255)),
                ('weight', models.IntegerField(choices=[(0, 'Decentralized'), (1, 'Semi-centralized'), (2, 'Centralized')], default=0)),
                ('validThrough', models.DateTimeField(auto_now_add=True)),
                ('UAI', models.CharField(blank=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OrderBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('transactionType', models.CharField(choices=[('currency', 'Currency'), ('assetGenesis', 'Asset Genesis'), ('assetTransfer', 'Asset Transfer'), ('assetSwap', 'Asset Swap'), ('assetProbe', 'Asset Probe')], max_length=50)),
                ('sender', models.CharField(max_length=255)),
                ('receipeint', models.CharField(max_length=255)),
                ('amount', models.IntegerField()),
                ('confirmations', models.IntegerField(blank=True)),
                ('transactionId', models.CharField(blank=True, max_length=255)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('makerAsset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='makerAsset', to='interest.Asset')),
                ('takerAsset', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='takerAsset', to='interest.Asset')),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
        migrations.AddField(
            model_name='orderbook',
            name='mempool',
            field=models.ManyToManyField(blank=True, to='interest.Transaction'),
        ),
    ]
