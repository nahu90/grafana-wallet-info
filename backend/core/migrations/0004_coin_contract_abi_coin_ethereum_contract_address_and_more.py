# Generated by Django 4.0.4 on 2022-05-12 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_coin_coinprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='coin',
            name='contract_abi',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='coin',
            name='ethereum_contract_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='coin',
            name='polygon_contract_address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
