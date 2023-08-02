from django.db import models
from django.db.models import UniqueConstraint, Q
from django.utils import timezone

from _db.utility import CreateHistoryModelMixin, SoftDeleteModelMixin, UpdateHistoryModelMixin, \
    CreationSensitiveModelMixin, BaseModel


class Subscriber(CreateHistoryModelMixin, SoftDeleteModelMixin, CreationSensitiveModelMixin, BaseModel):
    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='subscribers',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    ghased = models.ForeignKey(
        to='accounts.Ghased',
        related_name='subscribers',
        verbose_name='قاصد',
        on_delete=models.PROTECT,
    )

    def after_create(self):
        SubscriptionStatus.objects.create(subscriber=self)

    class Meta:
        constraints = (
            UniqueConstraint(
                fields=('ghased', 'channel'), condition=Q(is_deleted=False), name='unique_subscriber_if_not_deleted'
            ),
        )
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'


class SubscriptionStatus(CreateHistoryModelMixin, UpdateHistoryModelMixin, BaseModel):
    expires_at = models.DateTimeField(
        verbose_name='تاریخ انقضا',
        null=True, blank=True,
    )

    subscriber = models.OneToOneField(
        to='subscribe.Subscriber',
        related_name='subscription_status',
        on_delete=models.CASCADE,
        verbose_name='عضو کانال',
    )

    @property
    def is_premium(self):
        return bool(self.expires_at) and self.expires_at > timezone.now()


class PurchasedSubscription(CreateHistoryModelMixin, CreationSensitiveModelMixin, BaseModel):
    subscription = models.ForeignKey(
        to='channels.Subscription',
        related_name='purchased_subscriptions',
        on_delete=models.PROTECT,
        verbose_name='اشتراک',
    )

    subscriber = models.ForeignKey(
        to='subscribe.Subscriber',
        related_name='purchased_subscriptions',
        on_delete=models.PROTECT,
        verbose_name='عضو کانال',
    )

    def after_create(self):
        status = self.subscriber.subscription_status
        status.expires_at += self.subscription.duration
        status.save(update_fields=['expires_at'])

    class Meta:
        verbose_name = 'عضو کانال'
        verbose_name_plural = 'اعضای کانال‌ها'
