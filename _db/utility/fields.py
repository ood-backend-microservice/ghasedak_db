from django.core.validators import MinValueValidator, BaseValidator
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


def LocationCordinationField(**kwargs):
    """
    example:
        long/lat = LocationCordinationField(
            verbose_name='عرض جغرافیایی',
            null=True,
            blank=True,
        )
    """
    defaults = dict(
        max_digits=9,
        decimal_places=6,
    )
    defaults.update(kwargs)
    return models.DecimalField(
        defaults
    )


class PositiveFloatField(models.FloatField):
    default_validators = [MinValueValidator(0)]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'min_value': 0,
            **kwargs,
        })


class PercentageField(PositiveFloatField):
    default_validators = [*PositiveFloatField.default_validators, MinValueValidator(100)]

    def formfield(self, **kwargs):
        return super().formfield(**{
            'max_value': 100,
            **kwargs,
        })


@deconstructible
class GhasedakMobileNumberValidator(BaseValidator):
    message = _('Ensure your phone number has 11 digits starting with 09')
    code = 'mobile_number_value'

    def __init__(self, message=None):
        super().__init__(None, message)

    def compare(self, cleaned_value, limit_value):
        return cleaned_value.isnumeric() and len(cleaned_value) == 11 and cleaned_value.startswith('09')

    def clean(self, not_cleaned_value):
        return str(not_cleaned_value)
