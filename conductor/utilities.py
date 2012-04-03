from django.core.cache import cache

from itertools import izip_longest

def get_cache(key):
    return cache.get(key)

def set_cache(key, value, expiration=30):
    cache.set(key, value, expiration)

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)
