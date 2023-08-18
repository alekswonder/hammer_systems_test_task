import re

from django.core.exceptions import ValidationError

VALID_PHONE_NUMBER = re.compile(r'^\+?[1-9][0-9]{7,14}$')
PHONE_NUMBER_ERROR = 'Неверный номер телефона'


def validate_phone_number(phone_number):
    if not VALID_PHONE_NUMBER.fullmatch(phone_number):
        raise ValidationError(PHONE_NUMBER_ERROR)
