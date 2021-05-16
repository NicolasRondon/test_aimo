from hashlib import sha256
from random import random


def get_hexdigest(salt: str, raw_password: str) -> str:
    data = salt + raw_password
    return sha256(data.encode('utf8')).hexdigest()


def make_password(raw_password: str) -> str:
    salt = get_hexdigest(str(random()), str(random()))[:5]
    hsh = get_hexdigest(salt, raw_password)
    return '%s$%s' % (salt, hsh)


def check_password(raw_password: str, enc_password) -> bool:
    salt, hsh = enc_password.split('$', 1)
    return hsh == get_hexdigest(salt, raw_password)
