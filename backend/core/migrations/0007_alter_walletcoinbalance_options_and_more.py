# Generated by Django 4.0.4 on 2022-05-13 22:16

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_walletcoinbalance'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='walletcoinbalance',
            options={'verbose_name': 'Wallet Coin Balance', 'verbose_name_plural': 'Wallet Coin Balances'},
        ),
        migrations.AddField(
            model_name='walletcoinbalance',
            name='date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
