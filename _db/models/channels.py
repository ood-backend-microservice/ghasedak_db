from django.db import models
from django.utils import timezone

from _db.utility import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Channel(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    name = models.CharField(
        unique=True,
        verbose_name='نام',
        max_length=256
    )

    description = models.TextField(verbose_name='بیوگرافی کانال')

    class Meta:
        verbose_name = 'کانال'
        verbose_name_plural = 'کانال‌ها'


class ChannelContent(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='contents',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    class Meta:
        verbose_name = 'محتوای کانال'
        verbose_name_plural = 'محتواهای کانال‌ها'


class Subscription(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    class DurationChoices:
        ONE_MONTH = 'one month'
        ONE_MONTH_FA = 'یک ماهه'
        THREE_MONTH = 'three month'
        THREE_MONTH_FA = 'سه ماهه'
        SIX_MONTH = 'six month'
        SIX_MONTH_FA = 'شش ماهه'
        TWELVE_MONTH = 'twelve month'
        TWELVE_MONTH_FA = 'دوازده ماهه'

        @classmethod
        def get_choices(cls):
            return (
                (cls.ONE_MONTH, cls.ONE_MONTH_FA),
                (cls.THREE_MONTH, cls.THREE_MONTH),
                (cls.SIX_MONTH, cls.SIX_MONTH),
                (cls.TWELVE_MONTH, cls.TWELVE_MONTH_FA),
            )

    duration_choice = models.CharField(
        max_length=128,
        choices=DurationChoices.get_choices(),
        verbose_name='دوره',
    )

    channel = models.ForeignKey(
        to='channels.Channel',
        related_name='subscriptions',
        verbose_name='کانال',
        on_delete=models.PROTECT,
    )

    @property
    def duration(self):
        return {
            self.DurationChoices.ONE_MONTH: timezone.timedelta(days=30),
            self.DurationChoices.THREE_MONTH: timezone.timedelta(days=3 * 30),
            self.DurationChoices.SIX_MONTH: timezone.timedelta(days=6 * 30),
            self.DurationChoices.TWELVE_MONTH: timezone.timedelta(days=12 * 30),
        }[self.duration_choice]

    class Meta:
        verbose_name = 'اشتراک'
        verbose_name_plural = 'اشتراک‌های کانال‌ها'
