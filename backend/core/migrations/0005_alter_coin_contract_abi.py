# Generated by Django 4.0.4 on 2022-05-12 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_coin_contract_abi_coin_ethereum_contract_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coin',
            name='contract_abi',
            field=models.TextField(blank=True, null=True),
        ),
    ]
