import random,string


def random_str(num=8):
    return ''.join(random.sample(string.ascii_letters + string.digits, num))
