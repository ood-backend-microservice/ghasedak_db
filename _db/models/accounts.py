from django.contrib.auth import get_user_model
from django.db import models

from _db.utility import GhasedakMobileNumberValidator
from _db.utility import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Ghased(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    user = models.OneToOneField(
        to=get_user_model(),
        related_name='ghased',
        on_delete=models.PROTECT,
        verbose_name='کاربر جنگو'
    )

    phone_number = models.CharField(
        max_length=13,
        verbose_name='شماره همراه',
        unique=True,
        validators=[GhasedakMobileNumberValidator()]
    )

    class Meta:
        verbose_name = 'قاصد'
        verbose_name_plural = 'قاصدها'
