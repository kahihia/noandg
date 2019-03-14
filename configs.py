import random
import string

BID_STATUS = (('Open', 'Open'), ('Accepted', 'Accepted'), ('Denied', 'Denied'))

QUOTE_STATUS = (('Open', 'Open'), ('Accepted', 'Accepted'), ('Denied', 'Denied'))


def random_code(size=8, chars=string.ascii_letters):
    return ''.join(random.choice(chars) for _ in range(size)).upper()


def random_number(size=8, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))
