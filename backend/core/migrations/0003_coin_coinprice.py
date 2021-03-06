# Generated by Django 4.0.4 on 2022-05-09 03:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_wallet'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('coingecko_id', models.CharField(blank=True, max_length=255, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Coin',
                'verbose_name_plural': 'Coins',
            },
        ),
        migrations.CreateModel(
            name='CoinPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('price', models.FloatField()),
                ('date', models.DateField()),
                ('coin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.coin')),
            ],
            options={
                'verbose_name': 'Coin price',
                'verbose_name_plural': 'Coin prices',
            },
        ),
    ]
