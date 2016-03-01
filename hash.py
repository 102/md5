from hashlib import md5 as _md5


def md5(string):
    m = _md5()
    m.update(string)
    return m.hexdigest()
