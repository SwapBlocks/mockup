# Generated by Django 2.1.2 on 2018-10-11 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0005_auto_20181011_0805'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='sender',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
