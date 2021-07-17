from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext as _


@deconstructible
class UnicodeMobileNumberValidator(validators.RegexValidator):
    regex = r'09(\d{9})$'
    message = _(
        'Enter a valid mobile number. This value may contain only numbers.'
    )
    flags = 0
