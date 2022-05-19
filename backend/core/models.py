from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _



class COIN_TYPE:
    ETHEREUM = 'ETHEREUM'
    POLYGON = 'POLYGON'
    ERC_20 = 'ERC_20'
    ATOKEN = 'ATOKEN'

    items = [
        (ETHEREUM, _('Ethereum')),
        (POLYGON, _('Polygon')),
        (ERC_20, _('ERC-20')),
        (ATOKEN, _('AToken')),
    ]
    values = dict(items)


class TimeStampedModel(models.Model):
    """
    An abstract base class model that provides self-updating
    ``created`` and ``modified`` fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    profile_image = models.ImageField(verbose_name=_('profile image'), blank=True, null=True)


class Coin(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=20, choices=COIN_TYPE.items)
    coingecko_id = models.CharField(max_length=255, blank=True, null=True)

    ethereum_contract_address = models.CharField(max_length=255, blank=True, null=True)
    polygon_contract_address = models.CharField(max_length=255, blank=True, null=True)
    contract_abi = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Coin')
        verbose_name_plural = _('Coins')

    def __str__(self):
        return f'{self.name} [{self.coingecko_id}]'


class CoinPrice(TimeStampedModel):
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateField()

    class Meta:
        verbose_name = _('Coin price')
        verbose_name_plural = _('Coin prices')

    def __str__(self):
        return f'{self.price} [{self.date}]'


class Wallet(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _('Wallet')
        verbose_name_plural = _('Wallets')

    def __str__(self):
        return f'{self.name} [{self.address}]'


class WalletCoinBalance(TimeStampedModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    balance = models.FloatField()
    usd_balance = models.FloatField(blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name = _('Wallet Coin Balance')
        verbose_name_plural = _('Wallet Coin Balances')

    def __str__(self):
        return f'{self.wallet} - {self.coin} - {self.balance}'


class WalletTotalBalance(TimeStampedModel):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    usd_balance = models.FloatField(blank=True, null=True)
    date = models.DateTimeField()

    class Meta:
        verbose_name = _('Wallet Total Balance')
        verbose_name_plural = _('Wallet Total Balances')

    def __str__(self):
        return f'{self.wallet} - {self.usd_balance}'


class Image(TimeStampedModel):
    name = models.CharField(max_length=255, blank=True, null=True)
    img = models.ImageField(upload_to='images', blank=True, null=True)

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')

    def __str__(self):
        return f'{self.name}'
