from typing import TYPE_CHECKING

from django.db import models

from _db.utility import CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel, \
    ConcreteActiveManager

if TYPE_CHECKING:
    from channels.models import Channel


class ChannelManager(CreateHistoryModelMixin, UpdateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    concrete_objects = ConcreteActiveManager()

    ghased = models.ForeignKey(
        to='_db.Ghased',
        related_name='%(class)s',
        verbose_name='قاصد',
        on_delete=models.PROTECT,
    )

    channel: "Channel"

    class Meta:
        verbose_name = 'گرداننده کانال'
        verbose_name_plural = 'گردانندگان کانال'


class ChannelOwner(ChannelManager):
    channel = models.OneToOneField(
        to='_db.Channel',
        related_name='owner',
        on_delete=models.PROTECT,
        verbose_name='کانال'
    )

    class Meta:
        verbose_name = 'مالک کانال'
        verbose_name_plural = 'مالکین کانال‌ها'


class ChannelAdmin(ChannelManager):
    channel = models.ForeignKey(
        to='_db.Channel',
        related_name='admins',
        on_delete=models.PROTECT,
        verbose_name='کانال'
    )

    class Meta:
        verbose_name = 'مالک کانال'
        verbose_name_plural = 'مالکین کانال‌ها'
