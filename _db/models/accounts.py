from django.contrib.auth.models import User
from django.db import models

from _db.utility import GhasedakMobileNumberValidator
from _db.utility import CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel


class Ghased(CreateHistoryModelMixin, SoftDeleteModelMixin, BaseModel):
    user = models.OneToOneField(
        to=User,
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

    to_be_removed = models.CharField(
        max_length=256,
    )

    class Meta:
        verbose_name = 'قاصد'
        verbose_name_plural = 'قاصدها'
