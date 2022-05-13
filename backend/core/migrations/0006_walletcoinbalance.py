# Generated by Django 4.0.4 on 2022-05-12 02:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_coin_contract_abi'),
    ]

    operations = [
        migrations.CreateModel(
            name='WalletCoinBalance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('balance', models.FloatField()),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.coin')),
                ('wallet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.wallet')),
            ],
            options={
                'verbose_name': 'Wallet',
                'verbose_name_plural': 'Wallets',
            },
        ),
    ]