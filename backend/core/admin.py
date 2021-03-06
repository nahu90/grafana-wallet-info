from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from core.models import User, Wallet, Coin, CoinPrice, WalletCoinBalance, Image, WalletTotalBalance


@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    search_fields = ('name', )
    list_filter = ('is_active', )
    list_display = (
        'id', 'username', 'first_name', 'last_name', 'email', 'date_joined', 'is_staff', 'is_active',
    )


@admin.register(Wallet)
class WalletAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'address', )
    list_filter = ('is_active', )
    list_display = (
        'id', 'name', 'address', 'is_active',
    )


@admin.register(Coin)
class CoinAdmin(ImportExportModelAdmin):
    search_fields = ('name', 'coingecko_id', )
    list_filter = ('is_active', )
    list_display = (
        'id', 'name', 'coingecko_id', 'type', 'is_active',
    )


@admin.register(CoinPrice)
class CoinPriceAdmin(ImportExportModelAdmin):
    list_filter = ('coin', )
    list_display = (
        'id', 'coin', 'price', 'date',
    )


@admin.register(WalletCoinBalance)
class WalletCoinBalanceAdmin(ImportExportModelAdmin):
    list_filter = ('coin', )
    list_display = (
        'id', 'wallet', 'coin', 'balance', 'usd_balance', 'date',
    )


@admin.register(WalletTotalBalance)
class WalletTotalBalanceAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'wallet', 'usd_balance', 'date', 'is_active',
    )


@admin.register(Image)
class ImageAdmin(ImportExportModelAdmin):
    list_display = (
        'id', 'name', 'img',
    )
