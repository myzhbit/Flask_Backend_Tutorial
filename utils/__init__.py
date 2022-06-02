def gen_random_salt(length=32):
    import random
    import string
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
