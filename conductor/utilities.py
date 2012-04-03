from django.core.cache import cache

from itertools import izip_longest

def get_cache(key):
    return cache.get(key)

def set_cache(key, value, expiration=30):
    cache.set(key, value, expiration)

def add_to_cached_set(key, value, expiration=30, is_node=False):
    xs = get_cache(key)

    if not xs:
        xs = []

    if value not in xs: 
        xs.append(value)

    if is_node:
        # remove expired nodes
        xs = [x for x in xs if get_cache(x)]

    set_cache(key, xs, expiration)
    return xs

def grouper(iterable, n, fillvalue=None):
    args = [iter(iterable)] * n
    return izip_longest(*args, fillvalue=fillvalue)
