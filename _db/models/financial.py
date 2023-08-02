from django.db import models
from django.db.models import Sum, F

from _db.utility import CreateHistoryModelMixin, UpdateHistoryModelMixin, CreationSensitiveModelMixin, BaseModel


class Wallet(CreateHistoryModelMixin, UpdateHistoryModelMixin, BaseModel):
    class Exception(Exception):
        pass

    ghased = models.OneToOneField(
        to='accounts.Ghased',
        related_name='wallet',
        on_delete=models.PROTECT,
        verbose_name='قاصد'
    )

    balance = models.PositiveBigIntegerField(
        verbose_name='موجودی',
        default=0,
    )

    def _actual_balance(self):
        return self.entries.aggregate(balance=Sum('amount'))['balance']

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None, check_balance=True):
        is_balance_being_changed = self.pk and (update_fields is None or 'balance' in update_fields)
        if check_balance and is_balance_being_changed:
            actual_balance = self._actual_balance()
            if self.balance != actual_balance:
                raise InvalidBalance(self, self.balance, actual_balance)
        return super(Wallet, self).save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name = 'کیف پول'
        verbose_name_plural = 'کیف پول‌ها'


class InvalidBalance(Wallet.Exception):
    def __init__(self, wallet, balance, actual_balance):
        super(InvalidBalance, self).__init__(
            f'wallet {wallet.id} has balance {balance} but it must have {actual_balance}',
        )


class Transaction(CreateHistoryModelMixin, BaseModel):
    class Meta:
        verbose_name = 'تراکنش'
        verbose_name_plural = 'تراکنش‌ها'


class TransactionEntry(CreateHistoryModelMixin, CreationSensitiveModelMixin, BaseModel):
    wallet = models.ForeignKey(
        to='financial.Wallet',
        related_name='entries',
        verbose_name='کیف‌ پول',
        on_delete=models.PROTECT,
    )
    transaction = models.ForeignKey(
        to='financial.Transaction',
        related_name='entries',
        verbose_name='تراکنش مربوطه',
        on_delete=models.PROTECT,
        null=True, blank=True,
    )
    amount = models.PositiveBigIntegerField(verbose_name='مقدار')

    def after_create(self):
        self.wallet.__class__.objects.update(balance=F('balance') + self.amount)

    class Meta:
        verbose_name = 'ورودی کیف‌ پول'
        verbose_name_plural = 'ورودی‌های کیف‌ پول'
