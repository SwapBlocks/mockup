# Generated by Django 2.1 on 2018-09-05 19:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='asset',
            name='validThrough',
            field=models.DateTimeField(),
        ),
    ]