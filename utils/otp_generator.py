from random import randrange


def generate_otp() -> str:
    return str(randrange(1000, 10000))
