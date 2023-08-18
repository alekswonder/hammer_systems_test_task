from random import choice
from string import ascii_lowercase, ascii_uppercase, digits

from django.db import connection

CODE_LENGTH: int = 6


def generate_invite_code() -> str:
    """Генерация случайной последовательности символов для реферального кода"""
    referral_codes: tuple = ()

    with connection.cursor() as cursor:
        cursor.execute('select distinct invite_code from users_customuser')
        referral_codes = tuple(map(lambda element: element[0],
                                   cursor.fetchall()))

    characters: str = (ascii_lowercase + digits + ascii_uppercase)
    tries: int = 0
    while True:
        if tries > 5:
            raise Exception('Много коллизий, больше пяти итераций')
        result: str = ''.join(choice(characters) for _ in range(CODE_LENGTH))
        if result not in referral_codes:
            return result
        tries += 1
