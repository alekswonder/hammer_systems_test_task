import re

from django.core.exceptions import ValidationError

VALID_PHONE_NUMBER = re.compile(r'^[7-8][0-9]{10}$')
PHONE_NUMBER_ERROR = ('Номер должен начинаться либо с 8,'
                      'либо с 7, но БЕЗ "+".')


def validate_phone_number(phone_number):
    if not VALID_PHONE_NUMBER.fullmatch(phone_number):
        raise ValidationError(PHONE_NUMBER_ERROR)
