# Generated by Django 2.1 on 2018-09-07 18:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0004_auto_20180905_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='registrationAsset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='registration', to='interest.Asset'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='makerAsset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='makerAsset', to='interest.Asset'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='takerAsset',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='takerAsset', to='interest.Asset'),
        ),
    ]